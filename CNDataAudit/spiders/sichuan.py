from functools import partial

import scrapy

from CNDataAudit.spiders import SpecificProvinceDataSpider
from CNDataAudit.spiders.specific_province_data_spider import OperationMode


class SichuanDataSpider(SpecificProvinceDataSpider):
    num_pages = 429
    name = 'sichuan'
    domain = 'www.scdata.net.cn'
    base_catalog_url = f'https://{domain}/oportal/catalog/'

    operation_mode = OperationMode.EXTRACT_METADATA

    def extract_metadata(self, response: scrapy.http.Response):
        _extract_with_xpath = partial(self.extract_with_xpath, response)
        list_info_xpath = '//div[@class="list-details"]//li[{}]/span/text()'
        metadata = {
            'name': _extract_with_xpath('//input[@id="cata_name"]/@value'),
            'id': _extract_with_xpath('//input[@id="cata_id"]/@value'),
            'URL': response.url,
            'owner': _extract_with_xpath(list_info_xpath.format(1)),
            'category': _extract_with_xpath(list_info_xpath.format(2)),
            'published': _extract_with_xpath(list_info_xpath.format(3)),
            'updated': _extract_with_xpath(list_info_xpath.format(4)),
            'frequency': _extract_with_xpath('//li[@name="basicinfo"]'
                                             '//tr[4]/td[2]/text()'),
        }

        sample_data_url = _extract_with_xpath('//tr[@fileformat="xls"]'
                                              '/td[last()]/a/@href')
        yield (response.follow(sample_data_url,
                               callback=self.parse_sample_data,
                               meta={'metadata': metadata})
               if sample_data_url
               else metadata)

    def parse_sample_data(self, response):
        _extract_all_with_xpath = partial(self.extract_all_with_xpath, response)
        column_names = _extract_all_with_xpath('//tr[1]/td/text()')
        sample_data_values = _extract_all_with_xpath('//tr[2]/td/text()')

        metadata = response.meta['metadata']
        metadata['sample_data'] = {col_name: value for col_name, value in
                                   zip(column_names, sample_data_values)}
        yield metadata
