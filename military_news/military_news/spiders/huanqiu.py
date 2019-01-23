# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem

class HuanqiuSpider(scrapy.Spider):
    name = 'huanqiu'
    allowed_domains = ['mil.huanqiu.com']
    # start_urls = ['http://mil.huanqiu.com/']
    def __init__(self):
        self.web_name='环球军事'

    def start_requests(self):
        url='http://mil.huanqiu.com/world/{}.html'
        for i in range(1,31):
            if i==1:
                newurl=url.format('index')
            else:
                newurl=url.format(i)
            yield scrapy.Request(newurl,method='GET',callback=self.parse_newslist)


    # 解析新闻url列表
    def parse_newslist(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        # //div[@class="fallsFlow"]/ul/li/h3/a/@href
        news_a=soup.select('div.fallsFlow ul li h3 a')
        new_urllist=[]
        for a in news_a:
            new_urllist.append(a.get('href'))

        for news_url in new_urllist:
            yield scrapy.Request(news_url,method='GET',callback=self.parse_news,meta={'news_url':news_url})


    # 解析新闻数据
    def parse_news(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        item=MilitaryNewsItem()

        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间
        news_from=self.web_name
        news_url=response.request.meta['news_url']
        title=soup.select('h1')[0].text

        # 新闻内容
        content_p=soup.select('div.la_con p')
        content_str_list = []
        for p in content_p:
            content_str_list.append(p.text)
        content = ''.join(content_str_list)

        # 发行日期
        reslease_date=soup.select('span.la_t_a')[0].text.split(' ')[0]

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item
