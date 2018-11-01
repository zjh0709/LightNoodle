from WebScrapy.ScrapyJob import ScrapyJob
import sys

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    scrapy_job = ScrapyJob()
    if cmd is None:
        scrapy_job.save_tu_share_prime_news_topic()
    elif cmd == "topic":
        scrapy_job.save_sina_report_topic(first_page=True)
        scrapy_job.save_east_money_report_topic(first_page=True)
        scrapy_job.save_jrj_news_topic(first_page=True)
        scrapy_job.save_jrj_report_topic(first_page=True)
        scrapy_job.save_tu_share_prime_news_topic()
    elif cmd == "all":
        scrapy_job.save_sina_report_topic()
        scrapy_job.save_east_money_report_topic()
        scrapy_job.save_jrj_news_topic()
        scrapy_job.save_jrj_report_topic()
        scrapy_job.save_tu_share_prime_news_topic()
    elif cmd == "content":
        scrapy_job.save_content()

