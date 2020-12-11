# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def clean_address(value):
    return re.split(r'\|', value)[0].strip()


class ZillowspiderItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(clean_address),
                           output_processor=TakeFirst()
                           )
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
