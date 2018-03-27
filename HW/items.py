# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HwItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title=scrapy.Field()
    user=scrapy.Field()
    like_start=scrapy.Field()
    date=scrapy.Field()
    reply=scrapy.Field()
    content=scrapy.Field()