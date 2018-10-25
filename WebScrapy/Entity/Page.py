class Page(object):

    def __init__(self, url: object,
                 code: object = None,
                 category: object = None,
                 domain: object = None) -> object:
        self.url = url
        self.code = code
        self.category = category
        self.domain = domain

    @staticmethod
    def create_pages(wizard, min_page, max_page, page):
        return [Page(url=wizard.format(page.code, i),
                     code=page.code,
                     category=page.category,
                     domain=page.domain)
                for i in range(min_page, max_page + 1)]

    def to_dict(self):
        attrs = ["url", "code", "category", "domain"]
        return {k: getattr(self, k) for k in attrs}
