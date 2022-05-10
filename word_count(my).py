"""
Суромкин А.С.
Использование MapReduce для подсчета количества словосочетаний в документе
"""

from typing import Tuple, List, Dict
import re

data_dict = {}

import os   #импортируем модуль с функциями для работы с операционной системой

path = "/Users/aleksei/Documents/БФУ/2_Семестр/Верещагин_Технологии.BigData/Tasks1-3/Texts"


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
                key = "Phrase" + str(i) + ":" +file
                value = line.split("\n")
                value = value[0]
                data_dict[key] = value
                i+=1
# print all the file names
for name in filelist:
    print(name)

print(data_dict)

# Создадим словарь служебных слов, которые будем отсеивать "Предлоги и союзы не учитываем".
# Разумеется, тут не полный список всех предлогов и союзов
Service_Words = ["а", "однако", "но", "или", "так", "при", "ради", "через", "так как", "-", ".", ",", ";", ":", "!",
                 "?",
                 "чтобы", "что", "потому", "*", "#", "чем", "если", "таким образом", "на", "и", "в"]


def main():
    full_map_res: List[Tuple[str, int]] = []
    for doc_id in data_dict.keys():
        doc_id, map_res = map_fn(doc_id, data_dict[doc_id])
        full_map_res += map_res

    shuffle_res = shuffle_fn(full_map_res)
    reduce_res = reduce_fn(shuffle_res)

    for word, value in reduce_res.items():
        print(f'{word}: {value}')


def map_fn(doc_id: str, data: str) -> Tuple[str, List[Tuple[str, int]]]:
    sorted_Data = ""
    for word in re.split('\s+', data.lower()):  ## добавили отсеивание предлогов, союзов и служебных символов
        if word in Service_Words:               #
            continue                            #
        else:                                   #аж до сюда
            sorted_Data += word + " "
    out_dict: List[Tuple[str, int]] = []
    Split = re.split('\s+', sorted_Data.lower())
    Phrase = list(zip(Split, Split[1:]))        #формируем фразы, объединяя слова
    for word in Phrase:
        word = word[0] + " " + word[1]
        out_dict.append((word, 1))
    return doc_id, out_dict

def shuffle_fn(items: List[Tuple[str, int]]) -> Dict[str, List[int]]:
    out_dict: Dict[str, List[int]] = {}
    for key, value in items:
        if key not in out_dict:
            out_dict[key] = [value, ]
        else:
            out_dict[key].append(value)
    return out_dict


def reduce_fn(items: Dict[str, List[int]]) -> Dict[str, int]:
    out_dict = {}
    for key, values in items.items():
        if key not in out_dict:
            out_dict[key] = sum(values)
        else:
            out_dict[key] += 1
    return out_dict


if __name__ == '__main__':
    main()
