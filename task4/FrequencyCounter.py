import os
import string

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
import re

nltk.download('stopwords')


def read_documents(folder):
    documents = []
    for i in range(100):
        filename = f'выкачка_{i}.html'
        with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
            documents.append(f.read())
    return documents


def get_lemmas_documents(documents):
    pattern = re.compile('[^а-яА-ЯёЁ]')
    mystem = Mystem()
    lemmas_documents = []
    for document in documents:
        text = pattern.sub(' ', document.lower())
        word_tokens = [mystem.lemmatize(word)[0] for word in word_tokenize(text) if word.isalnum()]
        stop_words = set(stopwords.words('russian') + list(string.punctuation))
        clean_tokens = [word for word in word_tokens if word not in stop_words]
        lemmas_documents.append(' '.join(clean_tokens))
    return lemmas_documents


class FrequencyCounter:
    def __init__(self):
        self.output_tokens_folder_name = os.path.dirname(__file__) + '/tokens'
        self.output_lemmas_folder_name = os.path.dirname(__file__) + '/lemmas'
        self.html_folder_name = os.path.dirname(__file__) + '/../task1/pump_pages'
        self.tokens_file_name = os.path.dirname(__file__) + '/../task2/output/tokens.txt'
        self.lemmas_file_name = os.path.dirname(__file__) + '/../task2/output/lemmas.txt'
        if not os.path.exists(self.output_tokens_folder_name):
            os.makedirs(self.output_tokens_folder_name)
        if not os.path.exists(self.output_lemmas_folder_name):
            os.makedirs(self.output_lemmas_folder_name)

    def calculate_tf_idf(self):
        documents = read_documents(self.html_folder_name)

        with open(self.tokens_file_name, 'r', encoding='utf-8') as f:
            tokens = [token.strip() for token in f.readlines()]

        tfidf_vectorizer = TfidfVectorizer(vocabulary=tokens, stop_words=stopwords.words('russian'), lowercase=True)
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        for i, tfidf_row in enumerate(tfidf_matrix):
            tfidf_values = tfidf_row.toarray()[0]
            output_filename = os.path.join(self.output_tokens_folder_name, f'tf_idf_{i}.txt')
            with open(output_filename, 'w', encoding='utf-8') as f:
                for token, tfidf_value in zip(tokens, tfidf_values):
                    if tfidf_value != 0:
                        f.write(f"{token} {tfidf_vectorizer.idf_[tfidf_vectorizer.vocabulary_[token]]} {tfidf_value}\n")

        with open(self.lemmas_file_name, 'r', encoding='utf-8') as file:
            lemmas = []
            for line in file:
                lemmas.append(line.split()[0])

        lemmas_documents = get_lemmas_documents(documents)
        tfidf_vectorizer_lemmas = TfidfVectorizer(vocabulary=lemmas, stop_words=stopwords.words('russian'),lowercase=True)
        tfidf_matrix_lemmas = tfidf_vectorizer_lemmas.fit_transform(lemmas_documents)

        for i, tfidf_row in enumerate(tfidf_matrix_lemmas):
            tfidf_values = tfidf_row.toarray()[0]
            output_filename = os.path.join(self.output_lemmas_folder_name, f'tf_idf_{i}.txt')
            with open(output_filename, 'w', encoding='utf-8') as f:
                for lemma, tfidf_value in zip(lemmas, tfidf_values):
                    if tfidf_value != 0:
                        f.write(f"{lemma} {tfidf_vectorizer_lemmas.idf_[tfidf_vectorizer_lemmas.vocabulary_[lemma]]} {tfidf_value}\n")


if __name__ == '__main__':
    frequencyCounter = FrequencyCounter()
    frequencyCounter.calculate_tf_idf()
