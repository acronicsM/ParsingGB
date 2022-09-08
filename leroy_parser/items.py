# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def processor_price(value: str):
    value = value.strip().replace(' ', '')
    value = int(value) if value.isdigit() else None
    return value


def processor_property_value(value: str):
    value = value.strip()
    value = value if value else None

    return value


class LeroyParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field(output_processor=TakeFirst())

    photo = scrapy.Field()

    price = scrapy.Field(input_processor=MapCompose(processor_price), output_processor=TakeFirst())
    d_price = scrapy.Field(input_processor=MapCompose(processor_price), output_processor=TakeFirst())

    property = scrapy.Field(input_processor=MapCompose(processor_property_value))
    value = scrapy.Field(input_processor=MapCompose(processor_property_value))
