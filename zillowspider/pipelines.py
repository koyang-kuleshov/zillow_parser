# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class ZillowspiderPipeline:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.db = client['zillow_parse']

    def process_item(self, item, spider):
        self.collection = self.db[spider.name]
        self.collection.insert_one(item)
        return item


class ImgPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for url in item.get('photos'):
            try:
                yield Request(url)
            except ValueError as err:
                print(err)
        return item

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
