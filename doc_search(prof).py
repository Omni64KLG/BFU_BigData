"""
    Пример подокументного поиска
"""

from collections import namedtuple
from typing import List, Dict
import re

st_query = 'Где купить доллары по 45 рублей'

page_contents = {'Microsoft.com': 'Доллары - это хорошо. Нам нужно больше долларов. Доллары, доллары, доллары',
                 'CNN.com': 'И мы тое любим доллары и рубли. Дайте нам большге рублей',
                 'RussiaToday.com': 'Здесь можно все купить и доллары тоже'}

Doc = namedtuple('doc', 'name weight length')
PL_item = namedtuple('pl_item', 'doc word weight')
Word = namedtuple('word', 'word weight')

docs: List[Doc] = []
PL: List[PL_item] = []
words: List[Word] = []


def main():
    fill_tables()
    res_docs = search(str_query=st_query)
    print_results(res_docs)


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


def print_results(scored: Dict[str, float]) -> None:
    for doc_id, weight in scored.items():
        print(f'doc = {doc_id}; weight = {weight}')


if __name__ == '__main__':
    main()