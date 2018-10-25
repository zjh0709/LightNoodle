import re
import traceback

import requests
from bs4 import BeautifulSoup

from WebScrapy.Domain.BaseDomain import BaseDomain
from WebScrapy.Entity.Page import Page
from WebScrapy.Entity.Article import Article


class Sina(BaseDomain):

    def __init__(self):
        super().__init__()
        self.report_topic_wizard = "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index" \
                                   ".phtml?symbol={}&t1=all&p={}"
        self.domain_name = "sina"

    def get_report_topic_by_page(self, page: Page):
        url_expr = re.compile("vip.stock.finance.sina.com.cn/q/go.php/vReport_Show/kind/search/rptid")
        r = requests.get(page.url, headers=self.headers)
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=url_expr)
        articles = [Article(url=link.get("href"),
                            title=link.get("title"),
                            code=page.code,
                            category=page.category,
                            domain=page.domain)
                    for link in links]
        page_buttons = soup.find_all("a", onclick=re.compile("set_page_num"))
        max_page = 1
        if page_buttons:
            last_onclick = page_buttons[-1].get("onclick")
            re_page_num = re.compile("(?<=set_page_num\(')(.*)?(?='\))")
            re_result = re_page_num.search(last_onclick)
            if re_result:
                max_page = int(re_result.group())
        pages = Page.create_pages(self.report_topic_wizard, 2, max_page,
                                  page=page)
        return articles, pages

    def get_report_detail_by_url(self, url: str):
        r = requests.get(url, headers=self.headers)
        r.encoding = "gb2312"
        attr = {}
        # noinspection PyBroadException
        try:
            soup = BeautifulSoup(r.text, "html.parser")

            content_select = soup.find("div", class_="content")
            if content_select:
                # title
                attr.setdefault("title", content_select.find("h1").text.strip()) \
                    if content_select.find("h1") else None
                # content
                attr.setdefault("content", content_select.find("div", class_="blk_container").text.strip()) \
                    if content_select.find("div", class_="blk_container") else None
                # author org public_date
                spans = [ele.text.strip() for ele in content_select.find("div", class_="creab").findAll("span")] \
                    if content_select.find("div", class_="creab") else []
                author = [span for span in spans if "研究员：" in span]
                org = [span for span in spans if "机构：" in span]
                public_date = [span for span in spans if "日期：" in span]
                attr.setdefault("author", author[0].lstrip("研究员：")) if author else None
                attr.setdefault("org", org[0].lstrip("机构：")) if org else None
                attr.setdefault("public_date", public_date[0].lstrip("日期：")) if public_date else None
        except Exception:
            traceback.print_exc()
        return attr
