from enum import Enum
from pathlib import Path
from dataclasses import dataclass

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class FileFormat(Enum):
    ALL = 'all'
    XLS = '1'
    XML = '2'
    JSON = '3'
    CSV = '4'
    RDF = '5'
    API = '6'
    LINK = '7'
    OTHER = '8'

    def __str__(self):
        return self.value

    def extension_name(self):
        return FileFormat.extension_map().get(self, 'txt')

    @staticmethod
    def extension_map():
        valid_formats = {FileFormat.XLS, FileFormat.XML, FileFormat.JSON, FileFormat.CSV,
                         FileFormat.RDF}
        return {f: f.name.lower() for f in FileFormat if f in valid_formats}


class DataOpenType(Enum):
    ALL = 'all'
    UNRESTRICTED = '1'
    RESTRICTED = '2'

    def __str__(self):
        return self.value


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


def extract_with_xpath(response, xpath):
    return response.xpath(xpath).extract_first().strip()


class GenericDataSpider(CrawlSpider):
    # Defaults
    num_pages = 20
    file_format = FileFormat.CSV
    open_type = DataOpenType.UNRESTRICTED

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
        download_url = self.extract_download_url(response)
        yield Request(download_url.url,
                      callback=self.save_file,
                      meta={'cata_name': download_url.cata_name})

    def extract_download_url(self, response):
        cata_id_xpath = '//input[@id="cata_id"]/@value'
        cata_name_xpath = '//input[@id="cata_name"]/@value'
        id_in_rc_xpath = (f'//tr[@fileformat="{self.file_format.extension_name()}"]/td'
                          '//*[contains(@class, "downloadFileLink")]/@id')

        return DatasetDownloadURL(base_url=f'{self.base_catalog_url}download',
                                  cata_id=extract_with_xpath(response, cata_id_xpath),
                                  cata_name=extract_with_xpath(response, cata_name_xpath),
                                  id_in_rc=extract_with_xpath(response, id_in_rc_xpath))

    def save_file(self, response):
        directory_path = Path(self.name)

        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)

        filename = response.meta.get('cata_name')
        file_path = directory_path / f'{filename}.{self.file_format.extension_name()}'
        file_path.write_bytes(response.body)
        self.log(f'Saved file {filename}')
