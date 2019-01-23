# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MilitaryNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_from = scrapy.Field()
    # 新闻链接
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 出版日期
    published_at = scrapy.Field()
    pass
