from pathlib import Path

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class DataGovSpider(CrawlSpider):
    name = 'datagov'
    start_urls = ['https://catalog.data.gov/dataset']

    rules = (
        # Rule to navigate to each dataset's page
        Rule(LinkExtractor(restrict_css='h3.dataset-heading a')),

        # Rule to find and download CSV files directly
        Rule(LinkExtractor(restrict_css='a.btn.btn-primary[data-format="csv"]'),
             callback='save_csv'),

        Rule(LinkExtractor(restrict_css='ul.pagination li.page-item a.page-link')),
    )

    def parse_csv(self, response):
        yield {
            'status': response.status,
            'url': response.url,
        }

    def save_csv(self, response):
        filename = response.url.split('/')[-1].split('?')[0]
        Path(f'output/{filename}').write_bytes(response.body)
        self.log(f'Saved file {filename}')
