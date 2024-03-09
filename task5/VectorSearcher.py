import re
import numpy as np
from os import listdir, path
from pymystem3 import Mystem
from nltk.tokenize import word_tokenize
from scipy.spatial import distance


def read_links(file_name):
    links = dict()
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            index, value = line.split(' ')
            links[index] = value
    return links


def read_lemmas(file_name):
    lemmas = []
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            lemmas.append(line.split(' ')[0])
    return lemmas


def read_tf_idf(folder_name, lemmas):
    file_names = listdir(folder_name)
    matrix = np.zeros((len(file_names), len(lemmas)))
    for file_name in file_names:
        file_number = int(re.search('\\d+', file_name)[0])
        with open(folder_name + '/' + file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                lemma, idf, tf_idf = lines[i].split(' ')
                matrix[file_number - 1][lemmas.index(lemma)] = float(tf_idf)
    return matrix


class VectorSearcher:
    def __init__(self):
        self.index_file_name = path.dirname(__file__) + '/../task1/index.txt'
        self.lemmas_tf_idf_folder_name = path.dirname(__file__) + '/../task4/lemmas'
        self.lemmas_file_name = path.dirname(__file__) + '/../task2/output/lemmas.txt'
        self.links = read_links(self.index_file_name)
        self.lemmas = read_lemmas(self.lemmas_file_name)
        self.matrix = read_tf_idf(self.lemmas_tf_idf_folder_name, self.lemmas)
        self.mystem = Mystem()

    def vectorize(self, query: str) -> np.ndarray:
        vector = np.zeros(len(self.lemmas))
        tokens = word_tokenize(query.lower())
        for token in tokens:
            lemma = self.mystem.lemmatize(token)[0]
            if lemma in self.lemmas:
                vector[self.lemmas.index(lemma)] = 1
        return vector

    def search(self, query: str) -> list:
        vector = self.vectorize(query)
        similarities = dict()
        i = 1
        for row in self.matrix:
            dist = 1 - distance.cosine(vector, row)
            if dist > 0:
                similarities[i] = dist
            i += 1
        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        result = [self.links[str(doc[0])] for doc in sorted_similarities]
        return result


if __name__ == '__main__':
    vectorSearcher = VectorSearcher()
    print(vectorSearcher.search("конь"))
