# encoding=utf-8
import csv
import re
import requests
import traceback

from bs4 import BeautifulSoup
from time import sleep
import scrapy

def parse_hanzi():
    host_url = 'https://zidian.911cha.com'
    first_url = 'https://zidian.911cha.com/tongyongzi.html'
    headers = {
        'Referer': 'https://zidian.911cha.com/bushou.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
    }
    res = requests.get(first_url, headers=headers)
    res.encoding = 'utf-8'
    print(res.status_code)
    print(res.url)
    hanzi_list = []
    count = 0
    test = 0
    soup = BeautifulSoup(res.text, 'html.parser')
    panel_tag = soup.find("div", {"class": "leftbox"}).find_all("div", {"class": "panel"})[1]
    gclear_tags = panel_tag.find_all("div", {"class": "gclear"})
    for i in range(0, len(gclear_tags), 2):
        head_tag = gclear_tags[i]
        cont_tag = gclear_tags[i+1]
        a_tags = cont_tag.find("ul", {"class": "zi"}).find_all('a')
        bihua = head_tag.find('h3').text.split('笔画数为')[1].split('的')[0]
        tmp = int(head_tag.find('span').text.split('共')[1].split("字")[0])
        test += tmp
        # 判断是否有更多的标签
        last_tag = a_tags[-1]
        if last_tag.text == '更多»':
            # 有更多， 请求新的url
            more_url = host_url + '/' + last_tag.get('href')
            res2 = requests.get(more_url, headers=headers)
            res2.encoding = 'utf-8'
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            a_tags = soup2.find("ul", {"class": "zi"}).find_all("a")

        # 继续解析
        if tmp != len(a_tags):
            print(head_tag)
        for a_tag in a_tags:
            pinyin = a_tag.text[:-1]
            hanzi = a_tag.text[-1]
            single_url = host_url + '/' + a_tag.get('href')
            count += 1
            tmp_item = {
                "num": count,
                "bihua": bihua,
                "hanzi": hanzi,
                "pinyin": pinyin,
                "url": single_url,
            }
            hanzi_list.append(tmp_item)
    # break
    print(len(hanzi_list))
    print(test)

    file_path = './tongyongzi.csv'
    fields = [
        "num",
        "bihua",
        "hanzi",
        "pinyin",
        "url",
    ]
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fields)
        csv_writer.writeheader()
        csv_writer.writerows(hanzi_list)


if __name__ == "__main__":
    parse_hanzi()