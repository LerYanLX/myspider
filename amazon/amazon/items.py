# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    group_url = scrapy.Field()
    book_name = scrapy.Field()
    kindle_price = scrapy.Field()
    jin_price = scrapy.Field()
    pin_price = scrapy.Field()

    pass
