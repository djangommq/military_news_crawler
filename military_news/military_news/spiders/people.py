# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['military.people.com.cn']
    # start_urls = ['http://military.people.com.cn/']

    def __init__(self):
        self.web_name='人民网_'

    def start_requests(self):
        peop_urllist=[
            'http://military.people.com.cn/GB/367527/index{}.html',
            'http://military.people.com.cn/GB/1077/index{}.html'
        ]
        for peop_url in peop_urllist:
            for i in range(1,8):
                new_peopurl=peop_url.format(i)
                yield scrapy.Request(new_peopurl,method='GET',callback=self.parse_newsurllist)


    # 解析新闻url列表
    def parse_newsurllist(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        news_url_a=soup.select('div.ej_list_box.clear ul li a')
        # 新闻url列表
        news_url_list=[]
        for a in news_url_a:
            news_url_list.append('http://military.people.com.cn'+a.get('href'))

        # 新闻发行时间列表
        reslease_date_em=soup.select('div.ej_list_box.clear ul li em')
        reslease_date_list=[]
        for em in reslease_date_em:
            reslease_date_list.append(em.text)

        # 新闻类别名称
        cate_name=soup.select('div.lujing a:nth-of-type(3)')[0].text

        for i in range(len(news_url_list)):
            yield scrapy.Request(news_url_list[i],method='GET',callback=self.parse_news,meta={'cate_name':cate_name,'news_url':news_url_list[i],'reslease_date':reslease_date_list[i]})

    # 解析新闻数据
    def parse_news(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        item = MilitaryNewsItem()
        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间
        news_from=self.web_name+response.request.meta['cate_name']
        news_url=response.request.meta['news_url']
        title=soup.select('h1')[0].text

        # 内容
        content_p=soup.select('div.content.clear.clearfix p')
        if len(content_p)==0:
            content_p=soup.select('div.box_con p')
        content_str_list = []
        for p in content_p:
            content_str_list.append(p.text)
        content = ''.join(content_str_list)

        # 发行时间
        reslease_date=response.request.meta['reslease_date']

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item


