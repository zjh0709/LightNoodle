from WebScrapy.Domain.Sina import Sina
from WebScrapy.Domain.Jrj import Jrj
from WebScrapy.Domain.EastMoney import EastMoney
from WebScrapy.Domain.TuShare import TuShare


class A:
    def __init__(self):
        self.x = "x"
        self.y = "y"

    def to_dict(self):
        return {k: getattr(self, k) for k in ["x", "y"]}


print(A().to_dict())