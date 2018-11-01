from WebScrapy.Entity.Article import Article
from WebScrapy.Entity.Page import Page


class BaseDomain(object):
    def __init__(self):
        self.report_topic_wizard = str()
        self.report_content_wizard = str()
        self.news_topic_wizard = str()
        self.news_content_wizard = str()
        self.domain_name = str()
        self.max_page = 50
        self.NEWS = "news"
        self.REPORT = "report"

    @property
    def headers(self):
        return {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE7.0; WindowsNT5.1; Maxthon2.0)"
        }

    def first_report_topic_url(self, code: str = None):
        return Page(url=self.report_topic_wizard.format(code, 1),
                    code=code,
                    category=self.REPORT,
                    domain=self.domain_name)

    def get_report_topic_by_page(self, page: Page) -> tuple:
        pass

    def get_report_topic_by_code(self, code: str) -> list:
        first_page = self.first_report_topic_url(code)
        articles, pages = self.get_report_topic_by_page(first_page)
        if len(pages) >= self.max_page:
            return []
        for page in pages:
            other_articles, _ = self.get_report_topic_by_page(page)
            articles.extend(other_articles)
        return articles

    def get_report_topic_by_code_first_page(self, code: str) -> list:
        first_page = self.first_report_topic_url(code)
        articles, _ = self.get_report_topic_by_page(first_page)
        return articles

    def get_report_detail_by_url(self, url: str) -> dict:
        pass

    def detail_report(self, article: Article) -> Article:
        detail = self.get_report_detail_by_url(article.url)
        for k, v in detail.items():
            article.__setattr__(k, v)
        return article

    def first_news_topic_url(self, code: str = None):
        return Page(url=self.news_topic_wizard.format(code, 1),
                    code=code,
                    category=self.NEWS,
                    domain=self.domain_name)

    def get_news_topic_by_page(self, page: Page) -> tuple:
        pass

    def get_news_topic_by_code(self, code: str) -> list:
        first_page = self.first_news_topic_url(code)
        articles, pages = self.get_news_topic_by_page(first_page)
        for page in pages:
            other_articles, _ = self.get_news_topic_by_page(page)
            articles.extend(other_articles)
        return articles

    def get_news_topic_by_code_first_page(self, code: str) -> list:
        first_page = self.first_news_topic_url(code)
        articles, _ = self.get_news_topic_by_page(first_page)
        return articles

    def get_news_detail_by_url(self, url: str) -> dict:
        pass

    def detail_news(self, article: Article) -> Article:
        detail = self.get_news_detail_by_url(article.url)
        for k, v in detail.items():
            article.__setattr__(k, v)
        return article

    def get_prime_news_topic(self, page: Page):
        pass

    def get_prime_news_detail_by_url(self, url: str) -> dict:
        pass

    def detail_prime_news(self, article: Article) -> Article:
        detail = self.get_prime_news_detail_by_url(article.url)
        for k, v in detail.items():
            article.__setattr__(k, v)
        return article

    def get_trade_info(self, code, date=None) -> list:
        pass

    def get_current_trade_info(self) -> list:
        pass

    @property
    def stocks(self) -> list:
        pass

