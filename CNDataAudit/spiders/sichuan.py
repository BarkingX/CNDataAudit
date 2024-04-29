from CNDataAudit.spiders import GenericDataSpider


class SichuanDataSpider(GenericDataSpider):
    num_pages = 429
    name = 'sichuan'
    domain = 'www.scdata.net.cn'
    base_catalog_url = f'https://{domain}/oportal/catalog/'
