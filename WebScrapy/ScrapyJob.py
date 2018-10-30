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
        executor.map(save, articles).send(None)

    logging.info("end {} count {}".format(code, len(articles)))


def save_articles_by_func(f):
    logging.info("start")
    articles = f()
    io = NoodleIO()

    def save(article: Article):
        logging.info(article.code)
        io.save(table="article",
                data=article.to_dict(),
                spec_key=["url"])

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(save, articles).send(None)

    logging.info("end count {}".format(len(articles)))


class ScrapyJob(object):

    def __init__(self):
        self.sina = Sina()
        self.jrj = Jrj()
        self.east_money = EastMoney()
        self.tu_share = TuShare()
        self.stocks = self.tu_share.stocks

    def save_sina_report_topic(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(partial(save_articles_by_func_and_code, self.sina.get_report_topic_by_code), self.stocks)

    def save_jrj_news_topic(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(partial(save_articles_by_func_and_code, self.jrj.get_news_topic_by_code), self.stocks)

    def save_jrj_report_topic(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(partial(save_articles_by_func_and_code, self.jrj.get_report_topic_by_code), self.stocks)

    def save_east_money_report_topic(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(partial(save_articles_by_func_and_code, self.east_money.get_report_topic_by_code), self.stocks)

    def save_tu_share_prime_news_topic(self):
        save_articles_by_func(self.tu_share.get_prime_news_topic())
