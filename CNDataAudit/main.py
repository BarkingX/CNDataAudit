from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from CNDataAudit.spiders.sichuan import SichuanDataSpider


def run_spider(spider_cls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_cls)
    process.start()


if __name__ == '__main__':
    # run_spider(LiaoningDataSpider)
    run_spider(SichuanDataSpider)
