from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from CNDataAudit.spiders.datagov_spider import DataGovSpider


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DataGovSpider)
    process.start()


if __name__ == '__main__':
    run_spider()
