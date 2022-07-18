# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


def parsing_id(data: str, spider_name: str):
    if 'book24' in spider_name:
        return data.rpartition('-')[2].replace('/', '')
    elif 'labirint' in spider_name:
        return data[:-1].rpartition('/')[2].replace('/', '')

    return None


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.book1807

    def process_item(self, item: dict, spider):
        collections = self.mongo_base[spider.name]

        item['_id'] = parsing_id(item['link'], spider.name)
        item['name'] = self.parsing_name(item['name'])

        item['price'] = self.parsing_price(item['price'])
        item['currency'] = self.parsing_currency(item['currency'])
        item['d_price'] = self.parsing_price(item['d_price'])

        item['r_market'] = self.parsing_rating(item['r_market'])
        item['r_lib'] = self.parsing_rating(item['r_lib'])

        item['author'] = self.parsing_author(item['author'])
        item['isbn'] = self.parsing_isbn(item['isbn'])

        collections.update_one({'_id': item.get('_id')}, {'$set': item}, upsert=True)
        return item

    @staticmethod
    def parsing_name(data: str):
        return data.strip()

    @staticmethod
    def parsing_price(data: str):
        if data is not None:
            return float(data.replace(chr(8381), '').replace('\xa0', '').strip())

        return data

    @staticmethod
    def parsing_currency(data):
        if data == chr(8381):  # для '₽'
            return 'RUB'

        return data

    @staticmethod
    def parsing_rating(data):
        if data is not None:
            return float(data.replace(',', '.'))

        return data

    @staticmethod
    def parsing_author(data):
        if isinstance(data, str):
            return [data]  # Список удобнее

        return data

    @staticmethod
    def parsing_isbn(data: str):
        return data.replace('ISBN:', '').strip()
