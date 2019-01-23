import requests

from bs4 import BeautifulSoup


def parse_authors():
    basic_url = 'https://so.gushiwen.org/authors/default.aspx'
    res = requests.get(basic_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sumpage = soup.find('label', {'id':'sumPage'}).text
    authors = []
    for i in range(1, int(sumpage)+2):
        params = {
            'p': str(i),
            'c': None,
        }
        res = requests.get(basic_url, params)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        name_tags = soup.find_all('b')
        for tag in name_tags:
            authors.append(tag.text+'\n')

    print(len(authors))
    file_path = './authors.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(authors)


if __name__ == "__main__":
    parse_authors()