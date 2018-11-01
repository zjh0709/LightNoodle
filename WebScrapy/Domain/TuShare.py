import tushare as ts

from WebScrapy.Domain.BaseDomain import BaseDomain
from WebScrapy.Entity.Article import Article
from WebScrapy.Entity.Price import Price


class TuShare(BaseDomain):

    def __init__(self):
        super().__init__()
        self.domain_name = "tushare"

    def get_prime_news_topic(self, page=None):
        df = ts.get_latest_news(top=2000, show_content=False)
        if df is not None:
            articles = [Article(url=d.get("url"),
                                title=d.get("title"),
                                classify=d.get("classify"),
                                public_date=d.get("time"),
                                category=self.NEWS,
                                domain=self.domain_name)
                        for d in df.to_dict(orient="records")]
        else:
            articles = []
        return articles

    def get_prime_news_detail_by_url(self, url: str):
        attr = {}
        content = ts.latest_content(url)
        attr.setdefault("content", content)
        return attr

    def get_trade_info(self, code, date=None):
        date = "" if date is None else date
        df = ts.get_k_data(code, start=date, end=date)
        trade_info = [Price(code=code,
                            date=d.get("date"),
                            opening=d.get("open"),
                            closing=d.get("close"),
                            high=d.get("high"),
                            low=d.get("low"),
                            volume=d.get("volume"))
                      for d in df.to_dict("record")]
        return trade_info

    def get_current_trade_info(self):
        df = ts.get_today_all()
        return []

    @property
    def stocks(self):
        df = ts.get_stock_basics()
        return list(df.index)
