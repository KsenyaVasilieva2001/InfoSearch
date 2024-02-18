import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


def get_text_from_page(url):
    request = requests.get(url)
    if request.status_code == 200:
        soup = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
        return str(soup)
    return None


class Crawler:
    def __init__(self):
        self.pages_folder_name = os.path.dirname(__file__) + '/pump_pages'
        self.url_file_name = os.path.dirname(__file__) + '/links.txt'
        self.index_file_name = os.path.dirname(__file__) + '/index.txt'
        os.mkdir(self.pages_folder_name)

    def download_page(self):
        url_list = list(open(self.url_file_name, 'r', encoding='utf-8').read().split('\n'))
        index_file = open(self.index_file_name, 'w', encoding='utf-8')

        for i in range(0, len(url_list)):
            text = get_text_from_page(url_list[i])
            if text is None:
                continue
            else:
                page_name = self.pages_folder_name + '/выкачка_' + str(i) + '.html'
                page = open(page_name, 'w', encoding='utf-8')
                page.write(text)
                page.close()
                index_file.write(str(i) + ' ' + url_list[i] + '\n')


if __name__ == '__main__':
    crawler = Crawler()
    crawler.download_page()
