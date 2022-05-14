"""
    Суромкин А.С.
    Ранг документов
"""

from collections import namedtuple
from typing import List, Dict
import re

alpha = 0.15 #коэффициент случайного вхождения на сайт
StaticRank = namedtuple('StaticRank', 'name rank')
static_ranks: List[StaticRank] = [StaticRank(name='Толстой.txt', rank=100),
                                  StaticRank(name='Достоевский.txt', rank=100),
                                  StaticRank(name='Карамзин.txt', rank=50),
                                  StaticRank(name='Шолохов.txt', rank=75)]

dict_query = {} #Для задания ранга каждому слову запроса

RankLink = {} #Ранг ссылки одного документа
RankOutLink = {} #Ранг документа от внешних ссылок на него

RankWord_fromQuery = {} #ранг слов внутри документа

AbsoluteRank = {} #итоговый абсолютный рейтинг документа

import os   #импортируем модуль с функциями для работы с операционной системой

path = "/Users/aleksei/Documents/БФУ/2_Семестр/Верещагин_Технологии.BigData/Tasks1-3/WebSites"

page_contents = {}

filelist = []
for root, dirs, files in os.walk(path): #здесь мы открываем все директории и поддиректории и просматриваем документы
    for file in files:
        if file == ".DS_Store": continue #я работаю на MacOS => (Файл «.DS_Store» - это скрытый файл, созданный Mac OS X, и у него есть скрытая папка в видимой папке.)
        # append the file name to the list
        filelist.append(os.path.join(file))
        innerPath = root + "/" + file
        with open(innerPath) as File:
            for line in File:
                key = file
                value = line
                page_contents[key] = value
print(page_contents)

def MainQuery(Query):
    query = Query.lower().split(' ')
    return query

def Rank_words_of_query(query): #Добавляем ранг каждому отдельному слову запроса
    weight_of_word = 10
    for word in query:
        dict_query[word] = weight_of_word
    return dict_query    #в идеале можно ещё добавить отсеивание предлогов, союзов и служебных символов

def Rank_links_of_documents():
    for link in static_ranks:
        RankLink[link.name] = link.rank / 5 #пусть ссылка на документ внутри
    return RankLink  # другого документа будет придавать ранг делённый на 5 от изначального ранга страницы (StaticRank)


def DocRank_from_other_links(): #посчитаем ранг документа с учётом ссылок на него из других документов
    RankOutLink = RankLink.copy()
    for keys in RankOutLink.keys(): #обнулим все значения весов внешних ссылок на документ
        RankOutLink[keys] = 0
    for doc, words in page_contents.items():
        for word in re.split(" ", words):
           if word in RankOutLink.keys():
               RankOutLink[word] = RankOutLink[word] + RankLink[word] #будет справедливо давать ранг от
               RankOutLink[doc] = RankOutLink[doc] + RankLink[word] #перекрёстных ссылок и документу(в котором ссылка)
    return RankOutLink                                          #   и самой ссылке внтури этого документа

def DocRank_from_words():#посчитаем ранг документа с учётом вхождений слов внутри файла, относящихся к запросу
    RankWord_fromQuery = RankLink.copy()
    for keys in RankWord_fromQuery.keys(): #обнулим все значения весов от слов внутри документа
        RankWord_fromQuery[keys] = 0
    for doc, words in page_contents.items():
        for word in re.split(" ", words):
            if word in dict_query.keys():
                RankWord_fromQuery[doc] = RankWord_fromQuery[doc] + dict_query[word]
    return RankWord_fromQuery

def DocRank_from_RandomAccess_onPage():
    SumOfRanks = 0
    for link in static_ranks:
        SumOfRanks = SumOfRanks + link.rank
    return (1 - alpha) * SumOfRanks + alpha / len(static_ranks)

def AbsoluteDocRank(RankOutLink, RankWord_fromQuery, RandomAccess):
    AbsoluteRank = RankLink.copy()
    for keys in AbsoluteRank.keys(): #обнулим все значения весов от слов внутри документа
        AbsoluteRank[keys] = 0
    for link in static_ranks:
        key = link.name
        AbsoluteRank[key] = link.rank + RankOutLink[key] + RankWord_fromQuery[key] + RandomAccess
    return AbsoluteRank

def main():
    Raw_query = "Великий русский писатель"
    query = MainQuery(Raw_query)
    dict_query = Rank_words_of_query(query)
    print("dict_query: ", dict_query)
    RankLink = Rank_links_of_documents()
    print("RankLink: ", RankLink)
    RankOutLink = DocRank_from_other_links()
    print("RankOutLink", RankOutLink)
    RankWord_fromQuery = DocRank_from_words()
    print("RankWord_fromQuery: ", RankWord_fromQuery)
    RandomAссess = DocRank_from_RandomAccess_onPage()
    print("RandomAссess: ", RandomAссess)
    AbsoluteRank = AbsoluteDocRank(RankOutLink,RankWord_fromQuery,RandomAссess)
    print("-------------------------\nИтоговый рейтинг документов: ", AbsoluteRank)

if __name__ == '__main__':
    main()