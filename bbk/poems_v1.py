import csv
import re
import requests
import traceback
import random
import os
import logging

from bs4 import BeautifulSoup
from time import sleep

logFilename ='./bbk.log'

logging.basicConfig(
  level = logging.INFO,  # 定义输出到文件的log级别，
  format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
  datefmt= '%Y-%m-%d %A %H:%M:%S',  # 时间
  filename = logFilename,  # log文件名
  filemode = 'w'
)


class Poems(object):
    def __init__(self):
        self.basic_url = 'https://www.gushiwen.org'
        self.author_link_field = ['name', 'link']
        self.poem_field = [
            "name",
            "author_dynasty",
            "author_name",
            "content",
            "labels",
        ]
        self.basic_data_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.basic_data_dir):
            os.makedirs(self.basic_data_dir)

    def request(self, url):
        try:
            response = requests.get(url)
            sleep(random.choice(range(1,3)))
            if response.status_code == 200:
                logging.info('请求成功')
                return response.text
            else:
                logging.info('请求异常, 需要关注, 异常{}'.format(response.status_code))
                return None
        except Exception as e:
            logging.info('请求异常, 需要关注 {}, 异常{}'.format(url, e))
            return None

    def parse_author_links(self):
        url = 'https://www.gushiwen.org/shiwen/'
        res = self.request(url)
        if res is None:
            return None
        else:
            soup = BeautifulSoup(res, 'html.parser')
            authors = []
            a_tags = soup.find("div",{"id": "type2"}).find("div",{"class": "sright"}).find_all('a')
            for tag in a_tags:
                author_item = {
                    'name': tag.text,
                    'link': self.basic_url + tag.get('href'),
                }
                self.save_item('author_link', author_item)

    def save_item(self, type, item):
        field = []
        data_path = ''
        if type == 'author_link':
            field = self.author_link_field
            data_path = os.path.join(self.basic_data_dir, 'author_links.csv')
        elif type == 'poem':
            field = self.poem_field
            data_path = os.path.join(self.basic_data_dir, 'poems/{}.csv'.format(item.get('author_name')))
        else:
            return 0
        data_dir = os.path.split(data_path)[0]
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not os.path.exists(data_path):
            with open(data_path, 'w', encoding='utf-8', newline='') as f:
                csv_writer = csv.DictWriter(f, fieldnames=field)
                csv_writer.writeheader()
        with open(data_path, 'a', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=field)
            csv_writer.writerow(item)

    def parse_poem_item(self, res_content):
        soup = BeautifulSoup(res_content, 'html.parser')
        sons_tags = soup.find_all("div", {"class": "left"})[1].find_all("div", {"class": "sons"})
        for sons_tag in sons_tags:
            try:
                tmp_name = sons_tag.find('b').text
                a_tags = sons_tag.find("p", {"class": "source"}).find_all('a')
                tmp_author_dynasty = a_tags[0].text
                tmp_author_name = a_tags[1].text.strip()
                content = sons_tag.find("div", {"class": "contson"}).text.strip()
                # 中文括号改英文,换行去掉,把括号和里面的内容去掉
                content = content.replace(',', '，')
                content = content.replace('（', '(')
                content = content.replace('）', ')')
                content = content.replace('\r', '').replace('\n', '')
                tmp_content = re.sub('[(](.*)[)]', '', content)
                tag_tag = sons_tag.find("div", {"class": "tag"})
                if tag_tag is None:
                    tmp_labels = []
                else:
                    a_tags = sons_tag.find("div", {"class": "tag"}).find_all('a')
                    tmp_labels = [a_tag.text for a_tag in a_tags]

                poem_item = {
                    "name": tmp_name,
                    "author_dynasty": tmp_author_dynasty,
                    "author_name": tmp_author_name,
                    "content": tmp_content,
                    "labels": tmp_labels,
                }
                self.save_item('poem', poem_item)
            except Exception as e:
                logging.info(e, sons_tag)        

    def parse_poems_by_author(self, author_link_item):
        next_url = author_link_item.get('link')
        name = author_link_item.get('name')
        try:
            while next_url is not None:
                # 依次抓取下一页
                res = self.request(next_url)
                if res is None:
                    return None
                self.parse_poem_item(res)
                soup = BeautifulSoup(res, 'html.parser')
                sum_page = soup.find("label", {"id": "sumPage"}).text
                curr_page = soup.find("label", {"id": "temppage"}).text
                logging.info('正在获取作者: {} 的诗, 进度{}/{}页. '.format(name, curr_page, sum_page))
                amore_url = soup.find("a", {"class": "amore"}).get('href')
                if amore_url is None:
                    break
                next_url = self.basic_url + amore_url
            logging.info('获取作者: {} 的诗结束! '.format(name))
        except Exception as e:
            logging.info(e, traceback.format_exc())
            return None

    def load_author_links(self):
        author_links_path = os.path.join(self.basic_data_dir, 'author_links.csv')
        links = []
        try:
            with open(author_links_path, 'r', encoding='utf-8', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.author_link_field)
                for row in csv_reader:
                    if csv_reader.line_num == 1:
                        continue
                    links.append(dict(row))
        except Exception as e:
            logging.info('加载作者链接出现异常: {}'.format(e))
        finally:
            return links

    def parse_poems(self):
        links = self.load_author_links()
        for link in links:
            self.parse_poems_by_author(link)


if __name__ == "__main__":
    pomes = Poems()
    pomes.parse_author_links()
    pomes.parse_poems()