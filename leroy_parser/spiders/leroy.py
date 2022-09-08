import scrapy
from scrapy.http import HtmlResponse
from leroy_parser.items import LeroyParserItem as LpI
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/{kwargs.get('catalogue')}"]

    def parse(self, response: HtmlResponse):
        next = response.xpath("//div[@class='pager']//li//a[@class='next i-next']/@href").get()
        if next:
            yield response.follow(next, callback=self.parse)

        for link in response.xpath("//ul[contains(@class,'products-grid ')]//a[@class='product-card__img-link']"):
            yield response.follow(link, callback=self.page_parser)

    def page_parser(self, response: HtmlResponse):
        loader = ItemLoader(item=LpI(), response=response)
        loader.add_xpath('price', "//div[contains(@class,'add-to-cart__price')]//div[@class='current-price']//span//text()")
        loader.add_xpath('d_price', "//div[contains(@class,'add-to-cart__price')]//div[@class='old-price']//span//text()")
        loader.add_xpath('photo', "//li[contains(@class,'top-slide')]//@data-src")
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('property', "//dt[contains(@class,'specs-table__attribute-label')]//span/text()")
        loader.add_xpath('value', "//dd[contains(@class,'specs-table__attribute-value')]/text()")
        loader.add_xpath('_id', "//span[@itemprop='sku']/text()")
        loader.add_value('link', response.url)

        yield loader.load_item()
