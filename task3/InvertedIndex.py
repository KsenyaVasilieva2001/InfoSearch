import os
import nltk
import string
import pymorphy2
from os import listdir
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('stopwords')


class IndexInfo:
    def __init__(self):
        self.inverted_array = []

    def updateInfo(self, page):
        self.inverted_array.append(int(page))


class InvertedIndex:
    def __init__(self):
        self.output_folder_name = os.path.dirname(__file__) + '/output'
        self.html_folder_name = os.path.dirname(__file__) + '/../task1/pump_pages'
        self.lemmas_file_name = os.path.dirname(__file__) + '/../task2/output/lemmas.txt'
        self.lemmas_dict = dict()
        self.index_dict = dict()
        if not os.path.exists(self.output_folder_name):
            os.makedirs(self.output_folder_name)

    def get_lemmas_dict(self):
        lemmas_file = open(self.lemmas_file_name, 'r', encoding='utf-8')
        lines = lemmas_file.readlines()
        for line in lines:
            line_list = line.split()
            key = line_list[0]
            self.lemmas_dict[key] = []
            for i in range(1, len(line_list)):
                self.lemmas_dict[key].append(line_list[i])

    def get_inverted_index(self):
        for i in range(0, len(listdir(self.html_folder_name))):
            print(f"page in processing: {i + 1} ")
            page_name = listdir(self.html_folder_name)[i]
            page = open(self.html_folder_name + '/' + page_name, 'r', encoding='utf-8')
            text = BeautifulSoup(page, 'html.parser').get_text()
            tokenizer = RegexpTokenizer(r'\w+')
            list_text = tokenizer.tokenize(text)
            stops = set(stopwords.words('russian') + list(string.punctuation))
            morph = pymorphy2.MorphAnalyzer()
            for word in list_text:
                if word not in stops:
                    normal_word = morph.parse(word)[0].normal_form
                    if normal_word in self.lemmas_dict.keys():
                        if normal_word not in self.index_dict:
                            self.index_dict[normal_word] = IndexInfo()
                        self.index_dict[normal_word].updateInfo(i)
        for key, value in self.index_dict.items():
            value.inverted_array = list(set(value.inverted_array))

    def get_inverted_index_file(self):
        with open(os.path.join(self.output_folder_name, 'inverted_index.txt'), 'w', encoding='utf-8') as file:
            for key, entry in self.index_dict.items():
                str_array = " "
                for page in entry.inverted_array:
                    str_array = str_array + str(page) + " "
                file.write(key + str_array + '\n')


if __name__ == '__main__':
    inverted_index = InvertedIndex()
    inverted_index.get_lemmas_dict()
    inverted_index.get_inverted_index()
    inverted_index.get_inverted_index_file()
