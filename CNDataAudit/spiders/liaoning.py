from pathlib import Path
from dataclasses import dataclass

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

dataset_page_xpath = ('//*[contains(concat( " ", @class, " " ), '
                      'concat( " ", "cata-title", " " ))]/a[1]')


def get_start_urls():
    template = ('https://data.ln.gov.cn/oportal/catalog/'
                'index?fileFormat=4&openType=1&page={}')
    return [template.format(i) for i in range(1, 10)]


class LiaoningDataSpider(CrawlSpider):
    name = 'liaoning'
    allowed_domains = ['data.ln.gov.cn']
    start_urls = get_start_urls()
    rules = (
        Rule(LinkExtractor(restrict_xpaths=dataset_page_xpath), callback='parse_item'),
    )
    download_url_template = ('https://data.ln.gov.cn/oportal/catalog/'
                             'download?cataId={}&cataName={}&idInRc={}')
    base_download_url = 'https://data.ln.gov.cn/oportal/catalog/'

    def parse_item(self, response):
        def extract_with_xpath(xpath):
            return response.xpath(xpath).extract_first().strip()

        def construct_download_url():
            cata_id = extract_with_xpath('//input[@id="cata_id"]/@value')
            cata_name = extract_with_xpath('//input[@id="cata_name"]/@value')
            id_in_rc = extract_with_xpath('//tr[@fileformat="csv"]/td/a/@id')
            return DatasetDownloadURL(base_url=self.base_download_url, cata_id=cata_id,
                                      cata_name=cata_name, id_in_rc=id_in_rc)

        download_url = construct_download_url()
        # yield {'download_url': download_url.url}
        request = Request(download_url.url, callback=self.save_file)
        request.meta['cata_name'] = download_url.cata_name
        yield request

    def save_file(self, response):
        filename = response.meta.get('cata_name')
        Path(f'output/{filename}.csv').write_bytes(response.body)
        self.log(f'Saved file {filename}')


@dataclass
class DatasetDownloadURL:
    base_url: str
    cata_id: str
    cata_name: str
    id_in_rc: str

    @property
    def url(self):
        """Constructs and returns the full URL based on current parameters."""
        return (f'{self.base_url}?cataId={self.cata_id}&cataName={self.cata_name}'
                f'&idInRc={self.id_in_rc}')

    @property
    def name(self):
        """Returns the catalog name."""
        return self.cata_name
