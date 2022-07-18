import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem as BpI

search_query = 'd'


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']

    def __init__(self, search_query=None):
        self.start_urls = [f'https://www.labirint.ru/search/{search_query}/']

    def parse(self, response):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for i in response.xpath("//a[@class='cover']/@href"):
            yield response.follow(i.get(), callback=self.page_parser)

    def page_parser(self, response: HtmlResponse):
        detail = response.xpath("//div[@id='product']")[0]
        left = detail.xpath(".//div[@id='product-left-column']")[0]
        right = detail.xpath(".//div[@id='product-right-column']")[0]

        link = response.url
        name = detail.xpath(".//h1/text()").get()
        price = left.xpath(".//span[contains(@class,'buying-pricenew-val-number')]//text()").get()
        currency = left.xpath(".//span[contains(@class,'buying-pricenew-val-currency')]//text()").get()
        d_price = left.xpath(".//span[contains(@class,'buying-priceold')]//text()").get()
        author = left.xpath(".//a[@data-event-label='author']//text()").getall()
        isbn = left.xpath(".//div[@class='isbn']//text()").get()
        r_market = right.xpath(".//div[@id='rate']/text()").get()
        r_lib = None

        yield BpI(link=link, name=name, price=price, currency=currency, d_price=d_price, r_market=r_market, r_lib=r_lib, author=author, isbn=isbn)
