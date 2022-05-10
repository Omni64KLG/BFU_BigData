"""
    Суромкин А.С.
    Подокументный поиск
"""

from collections import namedtuple
from typing import List, Dict
import re

import os   #импортируем модуль с функциями для работы с операционной системой

path = "/Users/aleksei/Documents/БФУ/2_Семестр/Верещагин_Технологии.BigData/Tasks1-3/Links"

page_contents = {}

filelist = []
for root, dirs, files in os.walk(path): #здесь мы открываем все директории и поддиректории и просматриваем документы
    for file in files:
        if file == ".DS_Store": continue #я работаю на MacOS => (Файл «.DS_Store» - это скрытый файл, созданный Mac OS X, и у него есть скрытая папка в видимой папке.)
        # append the file name to the list
        filelist.append(os.path.join(file))
        innerPath = root + "/" + file
        with open(innerPath) as File:
            i = 1
            for line in File:
                key = file
                value = line
                page_contents[key] = value
                i+=1
print(page_contents)

queries = {     #будем делать не один, а несколько запросов по очереди(Для большей наглядности)
"st_query1" : "Компании",
"st_query2": "Железо",
"st_query3" : "Компании и железо",
"st_query4" : "дефицит"
}


Doc = namedtuple('doc', 'name weight length')
PL_item = namedtuple('pl_item', 'doc word weight')
Word = namedtuple('word', 'word weight')

docs: List[Doc] = []
PL: List[PL_item] = []
words: List[Word] = []

def main():
    fill_tables()
    for i in range(1,5):
        st_query = queries["st_query" + str(i)]
        res_docs = search(str_query= st_query)
        print_results(res_docs,i)


def fill_tables():
    for page, words in page_contents.items():
        words_dict = {}
        for word in re.split(r"[^\w']+", words.lower()):
            if word not in words_dict:
                words_dict[word] = 1
            else:
                words_dict[word] += 1

        for word, weight in words_dict.items():
            PL.append(PL_item(doc=page, word=word, weight=weight))


def search(str_query: str) -> Dict[str, float]:
    scored = {}
    query = str_query.lower().split(' ')
    for word in query:
        weight = 1
        for word_item in words:
            if word_item.word == word:
                weight = word_item.weight
                break
        for pl_item in PL:
            if pl_item.word == word:
                if pl_item.doc in scored:
                    scored[pl_item.doc] += pl_item.weight * weight
                else:
                    scored[pl_item.doc] = pl_item.weight * weight

    for doc_id in scored.keys():
        weight = 1
        length = 1
        for doc in docs:
            if doc.name == doc_id:
                weight = doc.weight
                length = doc.length
                break
        scored[doc_id] = scored[doc_id] * weight / length

    return scored


def print_results(scored: Dict[str, float], i) -> None:
    print("Запрос: " + queries["st_query" + str(i)])
    for doc_id, weight in scored.items():
        print(f'doc = {doc_id}; weight = {weight}')
    print("--------------------")

if __name__ == '__main__':
    main()