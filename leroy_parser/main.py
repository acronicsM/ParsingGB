from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings as gps
from scrapy.utils.log import configure_logging

from leroy_parser.spiders.leroy import LeroySpider

if __name__ == '__main__':
    catalogue = 'gardening-and-outdoor/gardening-equipment'

    configure_logging()
    runner = CrawlerRunner(gps())
    runner.crawl(LeroySpider, catalogue=catalogue)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
