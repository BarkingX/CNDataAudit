from unittest import TestCase

from CNDataAudit.spiders import GenericDataSpider


class TestDataSpider(TestCase):
    def test_construct_catalog_url(self):
        for spider_cls in GenericDataSpider.__subclasses__():
            spider = spider_cls()
            for num_page in range(1, spider.num_pages + 1):
                target = (f'{spider.base_catalog_url}'
                          f'index?fileFormat=4&openType=1&page={num_page}')
                self.assertEqual(target, spider.construct_catalog_url(num_page))
