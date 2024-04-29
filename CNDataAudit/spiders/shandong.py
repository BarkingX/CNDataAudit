from CNDataAudit.spiders import GenericDataSpider


class ShandongDataSpider(GenericDataSpider):
    # The DOM of page for dataset is updating dynamically using javascript
    # Unable to scrape easily......
    num_pages = 1
    name = 'shandong'
    domain = 'data.sd.gov.cn'
    base_catalog_url = f'https://{domain}/portal/catalog/'
