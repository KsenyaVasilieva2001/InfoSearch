import os
import pymorphy2
import re


class BooleanSearch:
    def __init__(self):
        self.inverted_index_file_name = os.path.dirname(__file__) + '/output/inverted_index.txt'
        self.index_dict = dict()
        self.morph = pymorphy2.MorphAnalyzer()

    def get_inverted_index_dict(self):
        inverted_index_file = open(self.inverted_index_file_name, 'r', encoding='utf-8')
        lines = inverted_index_file.readlines()
        for line in lines:
            line_list = line.split()
            key = line_list[0]
            files = set()
            self.index_dict[key] = files
            for i in range(1, len(line_list)):
                self.index_dict[key].add(line_list[i])

    def get_result(self, query):
        result_list = list()
        if type(query) != list:
            query_list = query.split()
        else:
            query_list = query
        for word in query_list:
            if (word == 'AND') | (word == 'OR') | (word == 'NOT'):
                result_list.append(word)
            elif type(word) == set:
                result_list.append(word)
            else:
                normal_word = self.morph.parse(word)[0].normal_form
                if normal_word in self.index_dict.keys():
                    res = self.index_dict[normal_word]
                    result_list.append(res)

        result = set(result_list[0])
        i = 1
        while i < len(result_list):
            if result_list[i] == 'AND' and i + 1 < len(result_list):
                other = set(result_list[i + 1])
                result = result & other
                i += 1
            elif result_list[i] == 'OR' and i + 1 < len(result_list):
                other = set(result_list[i + 1])
                result = result | other
                i += 1
            elif result_list[i] == 'NOT' and i + 1 < len(result_list):
                other = set(result_list[i + 1])
                result = result - other
                i += 1
            i += 1
        return result

    def search(self, query):
        query_list = [t.strip() for t in re.findall(r'.*?\S.*?(?:\b|$)', query)]
        while "(" in query_list:
            for index, i in enumerate(query_list):
                if i == ')':
                    count = index
                    for m in range(count, -1, -1):
                        if query_list[m] == '(':
                            bracket_list = query_list[m + 1:count]
                            bracket_str = " ".join(str(item) for item in bracket_list)
                            cur_result = self.get_result(bracket_str)
                            query_list[m:count + 1] = 'r'
                            query_list[:] = [set(cur_result) if x == 'r' else x for x in query_list]
        result = self.get_result(query_list)
        return sorted(result)


if __name__ == '__main__':
    boolean_search = BooleanSearch()
    boolean_search.get_inverted_index_dict()

    print(boolean_search.search('фантастика'))
    print(boolean_search.search('лиричность'))
    print(boolean_search.search('приписывают'))
    print(boolean_search.search('фантастика AND приписывают'))
    print(boolean_search.search('фантастика OR приписывают'))
    print(boolean_search.search('фантастика NOT приписывают'))
    print(boolean_search.search('фантастика AND лиричность'))
    print(boolean_search.search('фантастика OR лиричность'))
    print(boolean_search.search('фантастика OR рыбинске'))
    print(boolean_search.search('(фантастика OR рыбинске) AND (фантастика OR лиричность) AND фантастика'))
