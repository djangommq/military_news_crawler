import csv
import re
import requests
import traceback

from bs4 import BeautifulSoup
from time import sleep


def parse_bushou():
    url = 'https://zidian.911cha.com/bushou.html'
    host_url = 'https://zidian.911cha.com'
    headers = {
        'Referer': 'https://zidian.911cha.com/bushou.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
    }
    bushou_list = []
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    panel_tag = soup.find_all("div", {"class": "panel"})[1]
    gclear_tags = panel_tag.find_all("div", {"class": "gclear"})
    print(len(gclear_tags))
    count = 0
    for i in range(0, len(gclear_tags)-2, 2):
        head_tag = gclear_tags[i]
        cont_tag = gclear_tags[i+1]
        type = head_tag.text.split(' ')[1]
        a_tags = cont_tag.find_all('a')
        for a_tag in a_tags:
            bushou = a_tag.text[-1:]
            href = host_url + a_tag.get('href')[1:]
            res2 = requests.get(href, headers=headers)
            res2.encoding = 'utf-8'
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            tmp_name = soup2.find('h2').text
            tmp_name = tmp_name.replace('（', '(')
            tmp_name = tmp_name.replace('）', ')')
            name = re.sub('[(](.*)[)]', '', tmp_name)
            count += 1
            tmp_item = {
                "num": count,
                "type": type,
                "bushou": bushou,
                "name": name,
            }
            print(tmp_item)
            bushou_list.append(tmp_item)
    print(len(bushou_list))

    file_path = './bushou.txt'
    fields = [
        "num",
        "type",
        "bushou",
        "name",
    ]
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fields)
        csv_writer.writeheader()
        csv_writer.writerows(bushou_list)


if __name__ == "__main__":
    parse_bushou()