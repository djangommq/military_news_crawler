# -*- coding: utf-8 -*-
import re
import datetime
import scrapy
import requests
from bs4 import BeautifulSoup
from military_news.items import MilitaryNewsItem


class XiluSpider(scrapy.Spider):
    name = 'xilu'
    allowed_domains = ['junshi.xilu.com']
    # start_urls = ['http://junshi.xilu.com/']
    def __init__(self):
        self.web_name='西陆网'
        self.s_time_str = '2017-12-31'
        self.s_time = datetime.datetime.strptime(self.s_time_str, '%Y-%m-%d')
        # self.end_condition=True

    def start_requests(self):
        url='http://junshi.xilu.com/dfjs/index_{}.html'
        for pagenum in range(1,50):
            if pagenum==1:
                newurl='http://junshi.xilu.com/dfjs/index.html'
            elif pagenum>20:
                newurl='http://junshi.xilu.com/dfjs/index_1372_{}.html'.format(pagenum)
            else:
                newurl=url.format(pagenum)
            pagenum+=1
            yield scrapy.Request(newurl,method='GET',callback=self.parse_newslist)


    # 解析新闻url列表
    def parse_newslist(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        # //div[@class="newslist_box"]/ul/li/div[@class="newslist_tit"]/a/@href
        news_a=soup.select('div.newslist_box ul li div.newslist_tit a')
        news_urllist=[]
        for a in news_a:
            news_urllist.append(a.get('href'))

        for news_url in news_urllist:
            yield scrapy.Request(news_url,method='GET',callback=self.parse_news,meta={'news_url':news_url})



    # 解析新闻数据
    def parse_news(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        item=MilitaryNewsItem()

        # 网站名称 , 新闻url , 新闻标题 , 新闻内容 , 新闻发行时间

        # 发行日期
        reslease_date = soup.select('div.newsinfo_con div:nth-of-type(3)')[0].text.split(' ')[0]
        # 判断发行时间是否属于2018年
        reslease_time = datetime.datetime.strptime(reslease_date, '%Y-%m-%d')
        if reslease_time <= self.s_time:
            # self.end_condition = False
            return

        # 网站名称 , 新闻url , 新闻标题
        news_from=self.web_name
        news_url=response.request.meta['news_url']
        title=soup.select('h1')[0].text

        # 第一页内容
        content_onepage_p=soup.select('div.left.tagtext p')
        content_onepage_list = []
        for p in content_onepage_p:
            content_onepage_list.append(p.text)
        content_onepage = ''.join(content_onepage_list)

        # 其他页内容url
        content_otherpage_a=soup.select('div.page1.mt20 a')
        # 删除第一个和最后两个a标签
        content_otherpage_a.pop(0)
        content_otherpage_a.pop()
        content_otherpage_a.pop()
        # 取出剩余a标签的url
        content_otherpage_ulist=[]
        for a in content_otherpage_a:
            content_otherpage_ulist.append(a.get('href'))

        # 其他页面内容
        content_otherpage=self.parse_otherpage(content_otherpage_ulist)
        # 新闻总内容
        content=content_onepage+content_otherpage

        item['news_from'] = news_from
        item['url'] = news_url
        item['title'] = title
        item['content'] = re.sub(r'[\r\n]', '', content)
        item['published_at'] = reslease_date
        yield item

    # 解析其他页面的新闻内容
    def parse_otherpage(self,content_otherpage_ulist):
        content_otherpage=''
        if len(content_otherpage_ulist)==0:
            return content_otherpage

        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

        for other_url in content_otherpage_ulist:
            response=requests.get(other_url,headers=headers)
            response.encoding="gb2312"
            soup=BeautifulSoup(response.text,'lxml')

            # 解析新闻内容
            content_otherpage_p = soup.select('div.left.tagtext p')
            content_otherpage_list = []
            for p in content_otherpage_p:
                content_otherpage_list.append(p.text)
            content= ''.join(content_otherpage_list)

            content_otherpage=content_otherpage+content+'\n'

        return content_otherpage

