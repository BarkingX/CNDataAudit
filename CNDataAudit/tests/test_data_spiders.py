from unittest import TestCase

from CNDataAudit.spiders import SpecificProvinceDataSpider


class TestDataSpider(TestCase):
    def test_construct_catalog_url(self):
        for spider_cls in SpecificProvinceDataSpider.__subclasses__():
            spider = spider_cls()
            for num_page in range(1, spider.num_pages + 1):
                target = (f'{spider.base_catalog_url}'
                          f'index?fileFormat=4&openType=1&page={num_page}')
                self.assertEqual(target, spider.construct_catalog_url(num_page))

    # def test_extract_download_url_liaoning(self):
    #     ids = ['fceac2edb00c4e4f8fd9e0ffedf56692', '38833e459c284d03bf4a6b39fb8abe9f',
    #            'db07bc7a84ce4362b6fe4944cacd1ad6', '45e003262cf3493eb9e08c27d3000d3b']
    #     names = ['基金会登记信息', '基金会年检信息', '辽宁省儿童福利机构信息', '社会团体登记信息']
    #     ids_in_rc = ['EWdl9taVR/bpZxCLv8PV4rdE9Y1Jh3yQkXPRH/Ku8hZTjBDKB+lRZfRYbwx9QKgJ',
    #                  'X+9dL3Ey0aaVSoIBiXz+T2pCnjh/Tjhgs1+NQvyDFVJTjBDKB+lRZfRYbwx9QKgJ',
    #                  'ZA/+AX4SWQWsavC3746rp4j31L3xQD420nw9so2B51FTjBDKB+lRZfRYbwx9QKgJ',
    #                  'xs/ZFPqV6PFxTv6/ieCjz5Ajy3ifYeXThTlsrNfrk2VTjBDKB+lRZfRYbwx9QKgJ']
    #
    #
    #     spider = LiaoningDataSpider()
    #     download_urls = [DatasetDownloadURL(f'{spider.base_catalog_url}download',
    #                                         _id, name, id_in_rc)
    #                      for _id, name, id_in_rc in zip(ids, names, ids_in_rc)]
    #
    #     urls = [f'https://data.ln.gov.cn/oportal/catalog/{_id}' for _id in ids]
    #
    #     for url, download_url in zip(urls, download_urls):
    #         self.assertEqual(download_url.url, spider.extract_download_url(response=).url)
