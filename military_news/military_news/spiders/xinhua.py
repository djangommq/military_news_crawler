# -*- coding: utf-8 -*-
import re
import scrapy
import json
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem


class XinhuaSpider(scrapy.Spider):
    name = 'xinhua'
    allowed_domains = ['qc.wa.news.cn','xinhuanet.com']
    # start_urls = ['http://qc.wa.news.cn/']
    def __init__(self):
        self.web_name='新华军网_'
        # self.end_condition=True

    def start_requests(self):
        url_list=[
            # 'http://qc.wa.news.cn/nodeart/list?nid=11139635&pgnum={}&cnt=15&tp=1&orderby=1$中国',
            'http://qc.wa.news.cn/nodeart/list?nid=11139636&pgnum={}&cnt=15&tp=1&orderby=1$世界'
        ]
        for url in url_list:
            for pagenum in range(1,68):
                li=url.split('$')
                newurl=li[0].format(pagenum)
                yield scrapy.Request(newurl,method='GET',callback=self.parse_newslist,meta={'cate':li[1]})


    # 解析新闻url列表
    def parse_newslist(self, response):
        new_info_list=json.loads(response._cached_ubody[1:-1])['data']['list']
        news_urllist=[]
        for new in new_info_list:
            news_urllist.append(new['LinkUrl'])

        for news_url in news_urllist:
            yield scrapy.Request(news_url,method='GET',callback=self.parse_news,meta={'news_url':news_url,'cate':response.request.meta['cate']})


    # 解析新闻数据
    def parse_news(self,response):
        soup=BeautifulSoup(response.text)
        item=MilitaryNewsItem()

        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间
        news_from=self.web_name+response.request.meta['cate']
        news_url=response.request.meta['news_url']
        title=soup.select('h1')[0].text.replace('\r','').replace('\n','')

        # 新闻内容
        content_p=soup.select('div.article p')
        content_str_list = []
        for p in content_p:
            content_str_list.append(p.text)
        content = ''.join(content_str_list)

        # 发行时间
        reslease_date_str=soup.select('div.source span.time')[0].text.replace('\r','').replace('\n','')
        year, temp_str = reslease_date_str.split('年')
        month, temp_str = temp_str.split('月')
        day = temp_str.split('日')[0]
        reslease_date = year + '-' + month + '-' + day

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item