from enum import Enum, auto
from functools import partial
from pathlib import Path
from dataclasses import dataclass

import scrapy.http
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class OperationMode(Enum):
    DOWNLOAD = auto()
    EXTRACT_METADATA = auto()


class DataOpenType(Enum):
    ALL = 'all'
    UNRESTRICTED = '1'
    RESTRICTED = '2'

    def __str__(self):
        return self.value


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


@dataclass
class DatasetDownloadURL:
    base_url: str
    id: str
    name: str
    id_in_rc: str

    @property
    def url(self):
        """Constructs and returns the full URL based on current parameters."""
        return (f'{self.base_url}?cataId={self.id}&cataName={self.name}'
                f'&idInRc={self.id_in_rc}')


class SpecificProvinceDataSpider(CrawlSpider):
    # Defaults
    file_format = FileFormat.CSV
    open_type = DataOpenType.UNRESTRICTED
    operation_mode = OperationMode.DOWNLOAD
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="cata-title"]/a[1]'),
             callback='parse_dataset_page'),
    )

    # These should be overridden by subclasses
    num_pages = None
    name = None
    domain = None
    base_catalog_url = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [self.construct_catalog_url(i)
                           for i in range(1, self.num_pages + 1)]
        self.allowed_domains = [self.domain]

        self.operation_map = {
            OperationMode.DOWNLOAD: self.download_dataset,
            OperationMode.EXTRACT_METADATA: self.extract_metadata
        }

    @staticmethod
    def extract_with_xpath(response, xpath):
        result = response.xpath(xpath).get()
        return result.strip() if result else None

    @staticmethod
    def extract_all_with_xpath(response, xpath):
        result = response.xpath(xpath).getall()
        return [string.strip() for string in result] if result else None

    def construct_catalog_url(self, page_number):
        assert self.file_format == FileFormat.CSV

        return (f'{self.base_catalog_url}index?'
                f'fileFormat={self.file_format}&'
                f'openType={self.open_type}&'
                f'page={page_number}')

    def parse_dataset_page(self, response):
        return self.operation_map.get(self.operation_mode)(response)

    def download_dataset(self, response):
        download_url = self.extract_download_url(response)
        yield Request(download_url.url,
                      callback=self.save_file,
                      meta={'name': download_url.name})

    def extract_download_url(self, response):
        _extract_with_xpath = partial(self.extract_with_xpath, response)

        temp = '//input[@id="{}"]/@value'
        id_in_rc_xpath = (f'//tr[@fileformat="{self.file_format.extension_name()}"]/td'
                          '//*[contains(@class, "downloadFileLink")]/@id')
        return DatasetDownloadURL(base_url=f'{self.base_catalog_url}download',
                                  id=_extract_with_xpath(temp.format('cata_id')),
                                  name=_extract_with_xpath(temp.format('cata_name')),
                                  id_in_rc=_extract_with_xpath(id_in_rc_xpath))

    def save_file(self, response):
        directory_path = Path(self.name)

        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)

        filename = response.meta.get('name')
        file_path = directory_path / f'{filename}.{self.file_format.extension_name()}'
        file_path.write_bytes(response.body)
        self.log(f'Saved file {filename}')

    def extract_metadata(self, response):
        pass

    def parse_sample_data(self, response):
        pass
