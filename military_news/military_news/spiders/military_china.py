# -*- coding: utf-8 -*-
import scrapy


class MilitaryChinaSpider(scrapy.Spider):
    name = 'military_china'
    allowed_domains = ['military.china.com']
    start_urls = ['http://military.china.com/']

    def parse(self, response):
        pass
