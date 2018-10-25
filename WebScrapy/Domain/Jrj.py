import json
import re
import traceback

import math
import requests
import time
from bs4 import BeautifulSoup

from WebScrapy.Domain.BaseDomain import BaseDomain
from WebScrapy.Entity.Article import Article
from WebScrapy.Entity.Page import Page


class Jrj(BaseDomain):

    def __init__(self):
        super().__init__()
        self.news_topic_wizard = "http://stock.jrj.com.cn/share,{},ggxw_{}.shtml"
        self.report_topic_wizard = "http://istock.jrj.com.cn/yanbao_{}_p{}.html"
        self.domain_name = "jrj"

    def first_news_topic_url(self, code: str = None):
        return Page(url=self.news_topic_wizard.replace("_{}", "").format(code),
                    code=code,
                    category="news",
                    domain=self.domain_name)

    def get_news_topic_by_page(self, page: Page):
        url_expr = re.compile("http://stock.jrj.com.cn/\d{4}/\d{2}/\d+.shtml")
        r = requests.get(page.url)
        r.encoding = "gbk"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=url_expr)
        articles = [Article(url=link.get("href"),
                            title=link.text,
                            code=page.code,
                            category=page.category,
                            domain=page.domain)
                    for link in links]
        # page
        page_buttons = soup.find_all("a", href=re.compile("ggxw_\d+.shtml"))
        max_page = [int(b.text) for b in page_buttons if str(b.text).isdigit()][-1] \
            if page_buttons else 1
        pages = Page.create_pages(self.news_topic_wizard, 2, max_page,
                                  page=page)
        return articles, pages

    def get_news_detail_by_url(self, url: str):
        r = requests.get(url)
        r.encoding = "gbk"
        attr = {}
        # noinspection PyBroadException
        try:
            soup = BeautifulSoup(r.text, "html.parser")
            # content
            content_div = soup.find("div", class_="texttit_m1")
            content = ""
            for d in content_div.find_all(recursive=False):
                if "class" not in d.attrs:
                    content += d.text.strip()
            if content != "":
                attr.setdefault("content", content)
            # public_date org
            spans = soup.find("p", class_="inftop").find_all("span") \
                if soup.find("p", class_="inftop") else []
            spans = [span.text.strip() for span in spans]
            public_date = spans[0] if spans else None
            org = [span for span in spans if "来源：" in span]
            attr.setdefault("org", org[0].lstrip("来源：")) if org else None
            attr.setdefault("public_date", public_date) if public_date else None
        except Exception:
            traceback.print_exc()
        return attr

    def first_report_topic_url(self, code: str = None):
        return Page(url=self.report_topic_wizard.format(code, 1),
                    code=code,
                    category="report",
                    domain=self.domain_name)

    def get_report_topic_by_page(self, page: Page):
        url_expr = re.compile("http://istock.jrj.com.cn/article,yanbao,\d+.html")
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
        page_buttons = soup.find_all("a", href=re.compile("/yanbao_{}_p\d+.html".format(page.code)))
        max_page = 1
        try:
            max_page = max([int(p.text.lstrip("[").rstrip("]"))
                            for p in page_buttons if p.text.lstrip("[").rstrip("]").isdigit()])
        except ValueError:
            traceback.print_exc()
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
            # content
            replayContent_div = soup.find("div", id="replayContent")
            if replayContent_div:
                div = replayContent_div.find_all("div", limit=1)
                if div:
                    attr.setdefault("content", div[0].text.strip())
            # author, public_date
            p_title = soup.find("div", class_="lou").find("p", class_="title") \
                if soup.find("div", class_="lou") else None
            if p_title:
                p_title.find("span").decompose()
                attr.setdefault("author", p_title.find("a").text) if p_title.find("a") else None
                p_title.find("a").decompose()
                attr.setdefault("public_date", p_title.text.strip().lstrip("发表于").strip())
        except Exception:
            traceback.print_exc()
        return attr
