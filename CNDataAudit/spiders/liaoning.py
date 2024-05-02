from CNDataAudit.spiders import SpecificProvinceDataSpider


class LiaoningDataSpider(SpecificProvinceDataSpider):
    num_pages = 20
    name = 'liaoning'
    domain = 'data.ln.gov.cn'
    base_catalog_url = f'https://{domain}/oportal/catalog/'
