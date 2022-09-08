import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem as BpI


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']

    def __init__(self, search_query=None):
        self.start_urls = [f'http://book24.ru/search/?q={search_query}']

    def parse(self, response: HtmlResponse):

        if response.status == 200:
            if 'page' in response.url:
                page = response.url.find('page-')+5
                sl = response.url.find('/', page)
                paginator = int(response.url[page:sl])
                next_page = f'{response.url[:page]}{paginator+1}{response.url[sl:]}'
            else:
                next_page = response.url.replace('search/', 'search/page-2/')

            yield response.follow(next_page, callback=self.parse)

        x = "//div[contains(@class,'product-list catalog__product-list')]//a[contains(@class,'product-card__image-link')]/@href "
        for i in response.xpath(x):
            yield response.follow(i.get(), callback=self.page_parser)

    def page_parser(self, response: HtmlResponse):
        detail = response.xpath("//div[contains(@class,'product-detail-page__main-holder')]")[0]
        prices = detail.xpath(".//div[@class='product-detail-page__sidebar-holder']")
        property = detail.xpath(".//div[contains(@id, 'product-characteristic')]//li")

        link = response.url
        name = detail.xpath(".//h1/text()").get()
        price = prices.xpath(".//meta[@itemprop='price']/@content").get()
        currency = prices.xpath(".//meta[@itemprop='priceCurrency']/@content").get()
        d_price = prices.xpath(".//span[@class='app-price product-sidebar-price__price-old']/text()").get()
        r_market = detail.xpath(".//meta[@itemprop='ratingValue']/@content").get()
        r_lib = detail.xpath(".//div[contains(@class,'live-lib-widget')]//span[@class='rating-widget__main-text']").get()

        author = None
        isbn = None

        for i in property:
            characteristic = i.xpath(".//span[@class='product-characteristic__label']/text()").get().lower()
            value = i.xpath(".//div[@class='product-characteristic__value']//text()").get().strip()

            if 'автор' in characteristic:
                author = value.strip()
            elif 'isbn' in characteristic:
                isbn = value

        yield BpI(link=link, name=name, price=price, currency=currency, d_price=d_price, r_market=r_market, r_lib=r_lib, author=author, isbn=isbn)
