# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import logging
from military_news.items import MilitaryNewsItem
import datetime
import time
import re


class DstiSpider(scrapy.Spider):
    name = 'dsti'
    allowed_domains = ['www.dsti.net']
    # start_urls = ['http://www.dsti.net/']

    def __init__(self):
        self.base_name = '国防科技信息网_'
        self.base_url = 'http://www.dsti.net'
        self.input_url = {
            # '航天工业': 'http://www.dsti.net/Information/HyeList/spaceflight',
            '航空工业': 'http://www.dsti.net/Information/HyeList/aviation',
            '船舶工业': 'http://www.dsti.net/Information/HyeList/ship',
            '兵器工业': 'http://www.dsti.net/Information/HyeList/arms',
        }
        self.end_tag = False
        self.page = 0
        start_date_str = '2017-12-31'
        self.start_date = datetime.datetime.fromtimestamp(int(time.mktime(time.strptime(start_date_str, '%Y-%m-%d'))))


    def start_requests(self):
        for k, v in self.input_url.items():
            web_name = self.base_name + k
            self.page = 1
            self.end_tag = False
            while self.page < 55:
                url = v + '/{}'.format(self.page)
                print('url:{}'.format(url))
                self.page += 1
                request = scrapy.Request(url, method='GET', callback=self.parse_list)
                request.meta['web_name'] = web_name
                yield request

    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        news_tags = soup.find_all('a', {'class': 'a04'})
        for tag in news_tags:
            title = tag.text
            url = self.base_url + tag.get('href')
            print(title, url)
            request = scrapy.Request(url, method='GET', callback=self.parse_info)
            request.meta['web_name'] = response.meta.get('web_name')
            yield request

    def parse_info(self, response):
        if response.url != response.request.url:
            logging.info('网页被重定向到: {}'.format(response.url))
            return 0
        item = MilitaryNewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reslease_date_str = soup.find('div', {'class':'newsfrom'}).text.strip()
        reslease_date = datetime.datetime.fromtimestamp(int(time.mktime(time.strptime(reslease_date_str, '%Y-%m-%d'))))
        title = soup.find('div', {'class':'newsTitle'}).text.strip()
        if reslease_date < self.start_date:
            self.end_flag = True
            return
        content = soup.find('div', {'class':'newsContent'}).text
        new_url = response.url
        keyword = response.meta['web_name']
        item['news_from'] = keyword
        item['url'] = new_url
        item['title'] = title
        item['content'] =  re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item
