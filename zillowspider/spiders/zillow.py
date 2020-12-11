"""Источник: https://www.zillow.com

при старте паука передается список локаций которые необходимо обойти.

Необходимо обойти все объявления и собрать след структуру данных:

price - цена указанная в объявлении
address - поле адреса указанное в объвлении
photos - все фотографии из объявления в максимальном разрешении
( необходимо скачать и сохранить на компьютере)
"""

from time import sleep

import scrapy
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from zillowspider.items import ZillowspiderItem


class ZillowSpider(scrapy.Spider):
    """Spider for scraping zillow.com"""
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/']

    driver = webdriver.Firefox(
        executable_path='/usr/bin/geckodriver',
        firefox_binary='/usr/bin/firefox')

    def __init__(self, region: str, *args, **kwargs):
        self.start_urls = [f'{self.start_urls[0]}{region}/']
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """Main parse function"""
        real_estate = response.xpath('//a[@class="list-card-link"]/@href')
        for url in real_estate:
            yield response.follow(
                url,
                callback=self.get_real_estate_data
            )
        pages = response.xpath('//nav[@role="navigation"]/ul/li/a/@href')
        for page in pages:
            yield response.follow(page, callback=self.parse)

    def get_real_estate_data(self, response):
        """Method for parsing real estate data card"""
        item = ItemLoader(ZillowspiderItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('address',
                       '//head/title/text()'
                       )
        item.add_xpath('price',
                       ('//h3[contains(@class, "ds-price")]'
                        '//span[@class="ds-value"]/text()')
                       )
        self.driver.get(response.url)
        sleep(10)
        src_img = self.driver.find_elements_by_xpath(
            '//ul[contains(@class, "media-stream")]/li'
            '/button/picture/source[contains(@type, "image/jpeg")]'
        )
        media_col = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ds-media-col")]'
        )
        while True:
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            sleep(10)
            len_tmp = self.driver.find_elements_by_xpath(
                '//ul[contains(@class, "media-stream")]/li\
                /button/picture/source\
                [contains(@type, "image/jpeg")]'
            )
            if len(src_img) == len(len_tmp):
                break
            src_img = len_tmp
        spam = [itm.get_attribute('srcset').split(' ')[-2] for itm in
                self.driver.find_elements_by_xpath(
                '//ul[contains(@class, "media-stream")]'
                '/li/button/picture/source[contains(@type, "image/jpeg")]'
                )
                ]
        item.add_value('photos', spam)
        return item.load_item()
