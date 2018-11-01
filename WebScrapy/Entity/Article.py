class Article(object):

    def __init__(self,
                 url: str = None,
                 title: str = None,
                 content: str = None,
                 code: str = None,
                 public_date: str = None,
                 author: str = None,
                 classify: str = None,
                 org: str = None,
                 category: str = None,
                 domain: str = None,
                 **kwargs):
        self.url = url
        self.title = title
        self.content = content
        self.code = code
        self.public_date = public_date
        self.author = author
        self.classify = classify
        self.org = org
        self.category = category
        self.domain = domain

    @property
    def properties(self):
        return ["url", "title", "content", "code", "public_date",
                "author", "classify", "org", "category", "domain"]

    def to_dict(self):
        return {k: getattr(self, k) for k in self.properties
                if getattr(self, k) is not None}
