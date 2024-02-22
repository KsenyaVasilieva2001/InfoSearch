import string

import os

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymystem3 import Mystem
import re

nltk.download('punkt')
nltk.download('stopwords')


def extract_tokens_from_html(text):
    pattern = re.compile('[^а-яА-ЯёЁ]')
    text = pattern.sub(' ', text.lower())

    word_tokens = [word for word in word_tokenize(text) if word.isalnum()]
    stop_words = set(stopwords.words('russian') + list(string.punctuation))
    clean_tokens = [word for word in word_tokens if word not in stop_words]
    return clean_tokens


class Tokenizer:
    def __init__(self):
        self.output_folder_name = os.path.dirname(__file__) + '/output'
        self.html_folder_name = os.path.dirname(__file__) + '/../task1/pump_pages'
        if not os.path.exists(self.output_folder_name):
            os.makedirs(self.output_folder_name)

    def tokenize(self):
        tokens = set()
        lemmatized_tokens = {}
        for filename in os.listdir(self.html_folder_name):
            mystem = Mystem()
            if filename.endswith('.html'):
                with open(os.path.join(self.html_folder_name, filename), 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    extracted_tokens = extract_tokens_from_html(html_content)
                    for token in extracted_tokens:
                        tokens.add(token)
                        lemma = mystem.lemmatize(token)[0]
                        if lemma not in lemmatized_tokens:
                            lemmatized_tokens[lemma] = set()
                        lemmatized_tokens[lemma].add(token)

        with open(os.path.join(self.output_folder_name, 'tokens.txt'), 'w', encoding='utf-8') as file:
            for token in tokens:
                file.write(token + '\n')

        with open(os.path.join(self.output_folder_name, 'lemmas.txt'), 'w', encoding='utf-8') as file:
            for lemma, token_set in lemmatized_tokens.items():
                file.write(lemma + ' ' + ' '.join(token_set) + '\n')


if __name__ == '__main__':
    tokenizer = Tokenizer()
    tokenizer.tokenize()
