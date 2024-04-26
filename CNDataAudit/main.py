from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from CNDataAudit.spiders.liaoning import LiaoningDataSpider


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(LiaoningDataSpider)
    process.start()


if __name__ == '__main__':
    run_spider()
