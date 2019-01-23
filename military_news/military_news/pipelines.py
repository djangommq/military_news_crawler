# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
# import settings
from military_news.settings import MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER, MYSQL_PORT, MYSQL_PASSWORD
import pymysql
import os
import logging
import traceback


class MilitaryNewsPipeline(object):
    
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DATABASE,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            charset='utf8',
            use_unicode=True
        )

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "select id from military_news where url = '{}'".format(
                item['url'])
            )
            res = self.cursor.fetchone()
            if res:
                print('文章已存在')

            else:
                if item['author'] == None:
                    item['author'] = ''
                self.cursor.execute(
                    "insert into military_news (from_site, url, title, content, published_at) value(%s, %s, %s, %s, %s)",
                    (
                        item['news_from'],
                        item['url'],
                        item['title'],
                        item['content'],
                        item['published_at'],
                    )
                )
                self.connect.commit()
            return item
        except Exception as e:
            print(str(e))
            logging.info(str(e))

    def close_spider(self, spider):
        self.connect.close()


class NewsCsvPipeline(object):

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.field = [
            'news_from',
            'url',
            'title',
            'content',
            'published_at',
        ]

    def load_urls(self):
        urls = []
        try:
            with open(self.data_path, 'r', encoding='utf-8', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.field)
                for row in csv_reader:
                    if csv_reader.line_num == 1:
                        continue
                    urls.append(row.get('url'))
            return urls
        except Exception as e:
            print(e)
            return []

    def process_item(self, item, spider):
        try:
            self.data_path = os.path.join(self.data_dir, '{}.csv'.format(spider.name))
            if not os.path.exists(self.data_path):
                with open(self.data_path, 'w', encoding='utf-8', newline='') as f:
                    csv_writer = csv.DictWriter(f, fieldnames=self.field)
                    csv_writer.writeheader()
            
            all_urls = self.load_urls()
            if item.get('url') in all_urls:
                print('文章已存在')
            else:
                with open(self.data_path, 'a', encoding='utf-8', newline='') as f:
                    csv_writer = csv.DictWriter(f, fieldnames=self.field)
                    csv_writer.writerow(item)
            return item
        except Exception as e:
            print(str(e))
            logging.info(str(e))


class MySQLPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(
                host=MYSQL_HOST,
                db=MYSQL_DATABASE,
                user=MYSQL_USER,
                passwd=MYSQL_PASSWORD,
                port=MYSQL_PORT,
                charset='utf8',
                use_unicode=True
            )

    def open_spider(self, spider):
        # self.redis = StrictRedis(host='localhost', port=6379, db=4, password='')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        try:
            self.table = item.get('news_from')

            sql0 = 'CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY,news_from VARCHAR(100),url VARCHAR(100),title VARCHAR(100),content text,published_at VARCHAR(20))ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;'.format(self.table)
            self.cursor.execute(sql0)

            self.cursor.execute(
                    "select id from {} where url = '{}'".format(self.table, item['url'])
                )
            res = self.cursor.fetchone()
            if res:
                print('文章已存在')
            
            else:
                self.cursor.execute(
                        "insert into {} (news_from, url, title, content, published_at) value(%s, %s, %s, %s, %s)".format(self.table),
                        (
                            item['news_from'],
                            item['url'],
                            item['title'],
                            item['content'],
                            item['published_at'],
                        )
                    )
                self.db.commit()
                return item
                print('存储数据库{}'.format(self.table))
        except Exception as e:
            print(traceback.format_exc())
            print('异常：{}'.format(e))

    def close_spider(self,spider):
        self.db.close()

