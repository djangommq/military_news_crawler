import csv
import re
import requests
import traceback

from bs4 import BeautifulSoup
from time import sleep


def parse_saying():
    url = 'https://so.gushiwen.org/mingju/'
    basic_url = 'https://so.gushiwen.org'
    res = requests.get(url)
    print(res.status_code)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sort_tag = soup.find_all("div", {"class": "sons"})[2]
    a_tags = sort_tag.find_all('a')
    count = 0
    for a_tag in a_tags:
        tmp_url = basic_url + a_tag.get('href')
        saying_list = [
            a_tag.text + '\n',
        ]
        count += 1
        file_name = str(count) + '.csv'
        while True:
            res = requests.get(tmp_url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            content_tag = soup.find_all("div", {"class": "sons"})[0]
            cont_tags = content_tag.find_all("div", {"class": "cont"})
            for cont_tag in cont_tags:
                tmp_saying = cont_tag.find('a').text
                saying_list.append(tmp_saying + '\n')
            amore_tag = soup.find("a", {"class": "amore"})
            if amore_tag.get('href') is None:
                break
            tmp_url = basic_url + amore_tag.get('href')

        print(len(saying_list))
        file_path = './sayings/{}'.format(file_name)
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(saying_list)


if __name__ == "__main__":
    parse_saying()