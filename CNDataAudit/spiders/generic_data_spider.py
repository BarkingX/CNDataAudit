from pathlib import Path
from dataclasses import dataclass

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


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


def extract_with_xpath(xpath, response):
    return response.xpath(xpath).extract_first().strip()


class GenericDataSpider(CrawlSpider):
    # Defaults
    num_pages = 20
    file_format = 4
    open_type = '1'

    dataset_page_xpath = ('//*[contains(concat( " ", @class, " " ), '
                          'concat( " ", "cata-title", " " ))]/a[1]')
    rules = (
        Rule(LinkExtractor(restrict_xpaths=dataset_page_xpath),
             callback='parse_dataset_page'),
    )

    # These should be overridden by subclasses
    name = None
    domain = None
    base_catalog_url = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = [self.domain]
        self.start_urls = [self.construct_catalog_url(i)
                           for i in range(1, self.num_pages + 1)]

    def construct_catalog_url(self, page_number):
        return (f'{self.base_catalog_url}index?'
                f'fileFormat={self.file_format}&'
                f'openType={self.open_type}&'
                f'page={page_number}')

    def parse_dataset_page(self, response):
        download_url = self.construct_download_url(response)
        print(download_url.url)
        yield Request(download_url.url, callback=self.save_file,
                      meta={'cata_name': download_url.cata_name})

    def construct_download_url(self, response):
        cata_id = extract_with_xpath('//input[@id="cata_id"]/@value', response)
        cata_name = extract_with_xpath('//input[@id="cata_name"]/@value', response)
        id_in_rc = extract_with_xpath('//tr[@fileformat="csv"]/td/a/@id', response)

        return DatasetDownloadURL(base_url=f'{self.base_catalog_url}download',
                                  cata_id=cata_id, cata_name=cata_name, id_in_rc=id_in_rc)

    def save_file(self, response):
        filename = response.meta.get('cata_name')
        directory_path = Path(self.name)

        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)

        file_path = directory_path / f'{filename}.csv'
        file_path.write_bytes(response.body)
        self.log(f'Saved file {filename}')
