from concurrent.futures import ThreadPoolExecutor

from functools import partial

import logging

from WebScrapy.Domain.EastMoney import EastMoney
from WebScrapy.Domain.Jrj import Jrj
from WebScrapy.Domain.Sina import Sina
from WebScrapy.Domain.TuShare import TuShare
from WebScrapy.Entity.Article import Article
from WebScrapy.NoodleIO import NoodleIO


def save_articles_by_func_and_code(f, code: str):
    logging.info("start {}".format(code))
    articles = f(code)
    io = NoodleIO()

    def save(article: Article):
        logging.info(article.code)
        io.save(table="article",
                data=article.to_dict(),
                spec_key=["url"])

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(save, articles)

    logging.info("end {} count {}".format(code, len(articles)))


def save_articles_by_func(f):
    logging.info("start")
    articles = f()
    io = NoodleIO()

    def save(article: Article):
        logging.info(article.url)
        io.save(table="article",
                data=article.to_dict(),
                spec_key=["url"])

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(save, articles)

    logging.info("end count {}".format(len(articles)))


def save_content_by_funcs_and_articles(f_map={}, articles: list = []):
    logging.info("start")
    io = NoodleIO()

    def save(article: Article):
        logging.info(article.domain)
        article = f_map.get("{}_{}".format(article.domain, article.category),
                            lambda x: article)(article)
        if article.content is not None:
            io.save(table="article",
                    data=article.to_dict(),
                    spec_key=["url"])
        else:
            io.save(table="article",
                    data=article.to_dict(),
                    spec_key=["url"],
                    update_columns=["url"])

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(save, articles)

    logging.info("end count {}".format(len(articles)))


class ScrapyJob(object):

    def __init__(self):
        self.sina = Sina()
        self.jrj = Jrj()
        self.east_money = EastMoney()
        self.tu_share = TuShare()
        self.stocks = self.tu_share.stocks

    def save_sina_report_topic(self, first_page: bool=False):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if first_page:
                executor.map(partial(save_articles_by_func_and_code, self.sina.get_report_topic_by_code_first_page),
                             self.stocks)
            else:
                executor.map(partial(save_articles_by_func_and_code, self.sina.get_report_topic_by_code),
                             self.stocks)

    def save_jrj_news_topic(self, first_page: bool=False):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if first_page:
                executor.map(partial(save_articles_by_func_and_code, self.jrj.get_news_topic_by_code_first_page),
                             self.stocks)
            else:
                executor.map(partial(save_articles_by_func_and_code, self.jrj.get_news_topic_by_code),
                             self.stocks)

    def save_jrj_report_topic(self, first_page: bool=False):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if first_page:
                executor.map(partial(save_articles_by_func_and_code, self.jrj.get_report_topic_by_code_first_page),
                             self.stocks)
            else:
                executor.map(partial(save_articles_by_func_and_code, self.jrj.get_report_topic_by_code),
                             self.stocks)

    def save_east_money_report_topic(self, first_page: bool=False):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if first_page:
                executor.map(partial(save_articles_by_func_and_code, self.east_money.get_report_topic_by_code_first_page),
                             self.stocks)
            else:
                executor.map(partial(save_articles_by_func_and_code, self.east_money.get_report_topic_by_code),
                             self.stocks)

    def save_tu_share_prime_news_topic(self):
        save_articles_by_func(self.tu_share.get_prime_news_topic)

    def save_content(self):
        io = NoodleIO()
        f_map = {
            "{}_{}".format(self.sina.domain_name, self.sina.REPORT): self.sina.detail_report,
            "{}_{}".format(self.jrj.domain_name, self.jrj.REPORT): self.jrj.detail_report,
            "{}_{}".format(self.jrj.domain_name, self.sina.NEWS): self.jrj.detail_news,
            "{}_{}".format(self.east_money.domain_name, self.east_money.REPORT): self.east_money.detail_report,
            "{}_{}".format(self.tu_share.domain_name, self.tu_share.NEWS): self.tu_share.detail_news
        }
        data = io.load("article", limit=5000, order_by={"timestamp": 1})
        articles = [Article(**d) for d in data]
        save_content_by_funcs_and_articles(f_map, articles)
