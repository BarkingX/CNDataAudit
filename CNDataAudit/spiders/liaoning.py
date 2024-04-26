from CNDataAudit.spiders import GenericDataSpider


class LiaoningDataSpider(GenericDataSpider):
    num_pages = 10
    name = 'liaoning'
    domain = 'data.ln.gov.cn'
    base_catalog_url = f'https://{domain}/oportal/catalog/'
