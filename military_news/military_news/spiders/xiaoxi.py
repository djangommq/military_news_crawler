# -*- coding: utf-8 -*-
import re
import scrapy
import requests
import datetime
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem

class XiaoxiSpider(scrapy.Spider):
    name = 'xiaoxi'
    allowed_domains = ['cankaoxiaoxi.com']
    # start_urls = ['http://cankaoxiaoxi.com/']
    def __init__(self):
        self.web_name='参考消息_'
        self.s_time_str = '2017-12-31'
        self.s_time = datetime.datetime.strptime(self.s_time_str, '%Y-%m-%d')

    def start_requests(self):
        url_list=[
           'http://www.cankaoxiaoxi.com/mil/wqzb/{}.shtml',
           'http://www.cankaoxiaoxi.com/mil/zgjq/{}.shtml',
           'http://www.cankaoxiaoxi.com/mil/gjjq/{}.shtml'
        ]
        for url in url_list:
            for i in range(1,21):
                newurl=url.format(i)
                yield scrapy.Request(newurl,method='GET',callback=self.parse_newslist)


    # 解析新闻url列表
    def parse_newslist(self, response):
        soup=BeautifulSoup(response.text,'lxml')

        # 新闻所属类别
        cate=soup.select('div.crumb a:nth-of-type(3)')[0].text

        # //div[@class="inner"]/ul/li/a/@href
        news_a=soup.select('div.inner ul.txt-list-a.fz-14 li a')
        news_urllist=[]
        for a in news_a:
            news_urllist.append(a.get('href'))

        for news_url in news_urllist:
            yield scrapy.Request(news_url,method='GET',callback=self.parse_news,meta={'news_url':news_url,'cate':cate})

    def parse_news(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = MilitaryNewsItem()

        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间

        # 发行时间
        reslease_date=soup.select('span#pubtime_baidu')[0].text.split(' ')[0]
        # 判断发行时间是否属于2018年
        reslease_time = datetime.datetime.strptime(reslease_date, '%Y-%m-%d')
        if reslease_time <= self.s_time:
            return

        # 网站名称,新闻url,新闻标题
        news_from=self.web_name+response.request.meta['cate']
        news_url=response.request.meta['news_url']
        title=soup.select('h1')[0].text

        # 新闻内容
        content=self.parse_page(news_url)

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item


    # 新闻数据解析
    def parse_page(self, news_url):
        content= ''
        next_page=news_url

        while '.shtml' in next_page:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            }
            response=requests.get(next_page,headers=headers)
            response.encoding='utf-8'
            soup=BeautifulSoup(response.text,'lxml')

            # 获取该页内容
            content_p=soup.select('div.articleText p')
            if len(content_p)==0:
                # //div[@class="inner"]/div[@id="ctrlfscont"]/p
                content_p=soup.select('div.inner div#ctrlfscont p')
            content_str_list = []
            for p in content_p:
                content_str_list.append(p.text)
            content =content + '\n'.join(content_str_list)+'\n'

            # 解析下一页url
            next_a=soup.select('a#next_page')[0]
            next_page=next_a.get('href')

        return content