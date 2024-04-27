from unittest import TestCase

from CNDataAudit.spiders.liaoning import LiaoningDataSpider


class TestDataSpider(TestCase):
    def test_construct_catalog_url(self):
        spider = LiaoningDataSpider()
        for num_page in range(1, spider.num_pages + 1):
            target = ('https://data.ln.gov.cn/oportal/catalog/'
                      f'index?fileFormat=4&openType=1&page={num_page}')
            self.assertEqual(target, spider.construct_catalog_url(num_page))


