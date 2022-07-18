from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings as gps
from scrapy.utils.log import configure_logging

from bookparser.spiders.book24 import Book24Spider
from bookparser.spiders.labirint import LabirintSpider


if __name__ == '__main__':
    search_query = 'программирование'

    configure_logging()
    runner = CrawlerRunner(gps())
    runner.crawl(Book24Spider, search_query)
    runner.crawl(LabirintSpider, search_query)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
