import os
import logging
import csv
import re

logFilename ='./bbk.log'

logging.basicConfig(
  level = logging.INFO,  # 定义输出到文件的log级别，
  format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
  datefmt= '%Y-%m-%d %A %H:%M:%S',  # 时间
  filename = logFilename,  # log文件名
  filemode = 'a'
)

class ParsePoemName(object):
    def __init__(self):
        self.poem_field = [
                "name",
                "author_dynasty",
                "author_name",
                "content",
                "labels",
            ]
        self.basic_data_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/poems')
        self.basic_result_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
        if not os.path.exists(self.basic_result_dir):
            os.makedirs(self.basic_result_dir)

    def load_poems(self, file_path):
        poems = []
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.poem_field)
                for row in csv_reader:
                    if csv_reader.line_num == 1:
                        continue
                    poems.append(dict(row))
        except Exception as e:
            logging.info('加载诗词文件出现异常: {}, \n {}'.format(file_path, e))
        finally:
            return poems

    def parse_poems_to_line(self, poems):
        for poem in poems:
            title = poem.get('name')
            content = poem.get('content')
            self.save_title(title)
            self.save_content(content)

    def save_title(self, title):
        title_path = os.path.join(self.basic_result_dir, 'title.csv')
        logging.debug('修改前:{}'.format(title))
        title = title.strip().replace(' ', '').replace('·', '').replace('【', '').replace('】', '').replace('_', '').replace(',', '').replace('…', '').replace('，', '').replace('。', '').replace('、', '').replace('（', '').replace('）', '').replace('/', '').replace('《', '').replace('》', '')
        tmp_title = re.sub('[(](.*)[)]', '', title)
        logging.debug('修改后:{}'.format(tmp_title))
        with open(title_path, 'a', encoding='utf-8') as fw:
            fw.write(tmp_title + '\n')

    def save_content(self, content):
        content_path = os.path.join(self.basic_result_dir, 'content.csv')
        content = content.strip()
        items = re.split('[，。]', content)
        with open(content_path, 'a', encoding='utf-8') as fw:
            for item in items:
                if item.strip() == '':
                    continue
                fw.write(item + '\n')

    def run(self):
        files = os.listdir(self.basic_data_dir)
        logging.debug(len(files))
        for file in files:
            file_path = os.path.join(self.basic_data_dir, file)
            logging.debug('加载文件:{}'.format(file_path))
            poems = self.load_poems(file_path)
            self.parse_poems_to_line(poems)


if __name__ == '__main__':
    ppn = ParsePoemName()
    ppn.run()