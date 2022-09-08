import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint

dbName, Coll = 'news', 'news_col'
Ip, Port = 'localhost', 27017
Header = {'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
          'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05)'}


class MongoMy:
    def __init__(self):
        self._client = MongoClient(Ip, Port)
        self._db = self._client[dbName]
        self._coll = self._db[Coll]

    def update_one(self, document):
        self._coll.update_one({'_id': document.get('_id')}, {'$set': document}, upsert=True)

    def show_coll(self):
        pprint(list(self._coll.find({})))


def lenta_top_news():

    url = 'https://lenta.ru'

    session = requests.Session()
    response = session.get(url, headers=Header)

    if not response.ok:
        return False

    dom = html.fromstring(response.text)
    for i in dom.xpath("//a[contains(@class,'_topnews')]"):
        link = i.xpath("./@href")[0]
        name = i.xpath(".//h3/text()")
        source = 'lenta'
        date_pub = i.xpath(".//time/text()")

        v = {'_id': link,
             'link': link if 'https' in link else url + link,  # Иногода попадаются полные ссылки
             'name': str(name[0].replace('\xa0', '')) if name else '',
             'source': source,
             'date_publication': date_pub[0] if date_pub else ''}

        MongoMy().update_one(v)
        # ob_db.update_one({'_id': link}, {'$set': v}, upsert=True)


def yandex_top_news():
    url = 'https://yandex.ru/news/'

    session = requests.Session()
    response = session.get(url, headers=Header)

    if not response.ok:
        return False

    dom = html.fromstring(response.text)

    for i in dom.xpath("//section[contains(@aria-labelledby,'top-heading')]//div[contains(@class,'mg-grid__item')]"):
        link = i.xpath(".//h2/a/@href")[0]
        name = i.xpath(".//h2/a/text()")
        source = i.xpath(".//span[contains(@class,'mg-card-source__source')]/a/text()")
        date_pub = i.xpath(".//span[contains(@class,'mg-card-source__time')]/text()")

        v = {'_id': link,
             'link': link,
             'name': str(name[0]) if name else '',
             'source': str(source[0]) if source else '',
             'date_publication': date_pub[0] if date_pub else ''}

        MongoMy().update_one(v)
        # ob_db.update_one({'_id': link}, {'$set': v}, upsert=True)


def mail_top_news():
    url = 'https://news.mail.ru/'

    session = requests.Session()
    response = session.get(url, headers=Header)

    if not response.ok:
        return False

    dom = html.fromstring(response.text)

    for i in set(map(str, dom.xpath("//div[contains(@data-logger,'news__MainTopNews')]//a/@href"))):
        response = session.get(i, headers=Header)

        if not response.ok:
            continue

        hdr = html.fromstring(response.text).xpath("//div[contains(@class,'article__intro')]/..")[0]

        name = hdr.xpath(".//h1/text()")
        source = hdr.xpath(".//a/span/text()")
        date_pub = hdr.xpath(".//@datetime")

        v = {'_id': i,
             'link': i,
             'name': str(name[0]) if name else '',
             'source': str(source[0]) if source else '',
             'date_publication': date_pub[0] if date_pub else ''}

        MongoMy().update_one(v)
        # ob_db.update_one({'_id': link}, {'$set': v}, upsert=True)


if __name__ == '__main__':
    # client = MongoClient('localhost', 27017)
    # db = client['news']
    # news1 = db.news1
    lenta_top_news()
    yandex_top_news()
    mail_top_news()

    MongoMy().show_coll()
    # pprint(list(news1.find({})))
