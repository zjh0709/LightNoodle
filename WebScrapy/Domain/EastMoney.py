import json
import traceback

import requests
from bs4 import BeautifulSoup

from WebScrapy.Domain.BaseDomain import BaseDomain
from WebScrapy.Entity.Article import Article
from WebScrapy.Entity.Page import Page


class EastMoney(BaseDomain):

    def __init__(self):
        super().__init__()
        self.report_topic_wizard = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR" \
                                   "&code={}&p={}&ps=25&rt=51342638&js=%22data%22:[(x)],%22pages%22:%22(pc)%22," \
                                   "%22update%22:%22(ud)%22,%22count%22:%22(count)%22"
        self.domain_name = "eastmoney"

    def first_report_topic_url(self, code: str = None):
        return Page(url=self.report_topic_wizard.format(code, 1),
                    code=code,
                    category=self.REPORT,
                    domain=self.domain_name)

    def get_report_topic_by_page(self, page: Page):
        articles, max_page = [], 1
        try:
            r = requests.get(page.url, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            traceback.print_exc()
            return [], []
        r.encoding = "utf-8"
        try:
            data = json.loads("{"+r.text.strip().lstrip("(").rstrip(")")+"}")
            articles = [Article(url="http://data.eastmoney.com/report/{}/{}.html"
                                    .format(d.get("datetime")[:10].replace("-", ""), d.get("infoCode", "")),
                                author=d.get("author"),
                                public_date=d.get("datetime").replace("T", " "),
                                org=d.get("insName"),
                                title=d.get("title"),
                                code=page.code,
                                category=page.category,
                                domain=page.domain)
                        for d in data.get("data", [])]
            # page
            max_page = int(data.get("pages", 1))
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
        pages = Page.create_pages(self.report_topic_wizard, 2, max_page,
                                  page=page)
        return articles, pages

    def get_report_detail_by_url(self, url: str):
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            traceback.print_exc()
            return {}
        r.encoding = "gb2312"
        attr = {}
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", "newsContent")
        attr.setdefault("content", content.text) if content else None
        return attr
