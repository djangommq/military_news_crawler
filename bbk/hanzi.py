# encoding=utf-8
import csv
import re
import requests
import traceback

from bs4 import BeautifulSoup
from time import sleep


def parse_hanzi():
    host_url = 'https://zidian.911cha.com'
    headers = {
        'Referer': 'https://zidian.911cha.com/bushou.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
    }
    res = requests.get(host_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    panel_tag = soup.find("div", {"class": "rightbox"}).find_all("div", {"class": "gclear"})[1]
    urls = []
    a_tags = panel_tag.find_all('a')
    for a_tag in a_tags:
        tmp_url = a_tag.get('href')[1:]
        if a_tag.text == '笔画最多的字':
            continue
        bihua = a_tag.text[:-1]
        tmp_item = {
            "url": host_url + tmp_url,
            "bihua": bihua,
        }
        urls.append(tmp_item)

    hanzi_list = []
    count = 0

    for url in urls:
        res = requests.get(url.get("url"), headers=headers)
        res.encoding = 'utf-8'
        print(res.status_code)
        print(res.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        panel_tag = soup.find("div", {"class": "leftbox"}).find_all("div", {"class": "panel"})[1]
        gclear_tags = panel_tag.find_all("div", {"class": "gclear"})
        for i in range(0, len(gclear_tags), 2):
            head_tag = gclear_tags[i]
            cont_tag = gclear_tags[i+1]
            bushou = head_tag.find('h3').text.split('部首为')[1][0]
            a_tags = cont_tag.find("ul", {"class": "zi"}).find_all('a')
            bihua = url.get('bihua')
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
            for a_tag in a_tags:
                print('*******************', a_tag)
                if a_tag.find('img') is None:
                    # tmp_content = re.sub('[<a](.*)[>]', '', str(a_tag), 1)
                    # tmp_content = re.sub('[<span](.*)[</span>]', '', tmp_content, 2)
                    # hanzi = tmp_content.replace("</a>", '')
                    pinyin_tmp = a_tag.get('title')
                    if pinyin_tmp is None:
                        hanzi = a_tag.text[0]
                    else:
                        hanzi = a_tag.text.replace(pinyin_tmp.split('、')[0], '')[0]
                else:
                    # hanzi = a_tag.find('img').get('alt')
                    continue
                pinyin = a_tag.get('title')
                single_url = host_url+ '/' + a_tag.get('href')
                count += 1
                tmp_item = {
                    "num": count,
                    "bihua": bihua,
                    "bushou": bushou,
                    "hanzi": hanzi,
                    "pinyin": pinyin,
                    "url": single_url,
                }
                print(tmp_item)
                hanzi_list.append(tmp_item)
        # break
    print(len(hanzi_list))

    file_path = './hanzi.csv'
    fields = [
        "num",
        "bihua",
        "bushou",
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