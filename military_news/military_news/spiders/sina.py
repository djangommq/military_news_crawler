# -*- coding: utf-8 -*-
import re
import time
import datetime
import scrapy
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['mil.news.sina.com.cn']
    # start_urls = ['http://mil.news.sina.com.cn/']
    def __init__(self):
        self.web_name='新浪军事_'
        self.end_condition=True
        self.s_time_str='2017-12-31'
        self.s_time=datetime.datetime.strptime(self.s_time_str,'%Y-%m-%d')


    def start_requests(self):
        url_list=[
                'http://mil.news.sina.com.cn/roll/index.d.html?cid=57918&page={}',
                'http://mil.news.sina.com.cn/roll/index.d.html?cid=57919&page={}'
        ]
        # headers={
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6",
        #     "Cache-Control": "max-age=0",
        #     "Host": "mil.news.sina.com.cn",
        #     "If-Modified-Since": "Fri, 14 Dec 2018 06:28:00 GMT",
        #     "Proxy-Connection": "keep-alive",
        #     "Upgrade-Insecure-Requests": "1"
        # }
        for url in url_list:
            page=25
            while self.end_condition :
                new_url=url.format(page)
                page+=1
                yield scrapy.Request(new_url,method='GET',callback=self.parse_newslist)


    # 解析新闻urllist
    def parse_newslist(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        news_name=soup.select('h3')[0].text
        news_a=soup.select('div.fixList ul li a')
        if len(news_a)==0:
            self.end_condition = False
            return
        news_url=[]
        for a in news_a:
            news_url.append(a.get('href'))

        for url in news_url:
            request=scrapy.Request(url,callback=self.parse_news,meta={'news_name':news_name,'url':url})
            yield request



    # 解析新闻数据
    def parse_news(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        item=MilitaryNewsItem()
        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间
        news_from=self.web_name+response.request.meta['news_name']
        news_url=response.request.meta['url']
        title=soup.select('h1.main-title')[0].text

        content_p=soup.select('div.article p')
        content_str_list=[]
        for p in content_p:
            content_str_list.append(p.text)
        content='\n'.join(content_str_list)


        reslease_date_str=soup.select('span.date')[0].text.split()[0]
        year,temp_str=reslease_date_str.split('年')
        month,temp_str=temp_str.split('月')
        day=temp_str.split('日')[0]
        reslease_date=year+'-'+month+'-'+day

        # 判定新闻日期是否属于2018 , 否则改变
        reslease_date_obj=datetime.datetime.strptime(reslease_date,'%Y-%m-%d')
        if reslease_date_obj<self.s_time:
            self.end_condition = False
            return

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item



