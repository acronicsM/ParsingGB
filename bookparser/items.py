# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    d_price = scrapy.Field()
    r_market = scrapy.Field()
    r_lib = scrapy.Field()
    author = scrapy.Field()
    isbn = scrapy.Field()
