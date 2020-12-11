from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Settings

from zillowspider import settings
from zillowspider.spiders.config import region
from zillowspider.spiders.zillow import ZillowSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_proc = CrawlerProcess(settings=crawler_settings)

    crawler_proc.crawl(ZillowSpider, region)

    crawler_proc.start()
