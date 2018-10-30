# from WebScrapy.Domain.Sina import Sina
# from WebScrapy.Domain.Jrj import Jrj
# from WebScrapy.Domain.EastMoney import EastMoney
# from WebScrapy.Domain.TuShare import TuShare
# from WebScrapy.IO import IO
from WebScrapy.ScrapyJob import ScrapyJob


ScrapyJob().save_sina_report_topic()

#
# for article in articles:
#     io.save(table="article",
#             data=article.to_dict(),
#             spec_key=["url"])
#     print("success.")
