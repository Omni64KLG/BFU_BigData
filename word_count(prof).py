"""
Пример использования MapReduce для подсчета количества слов в документе
"""

from typing import Tuple, List, Dict
import re

data_dict = {'medvedev.txt': 'Свобода лучше, чем несвобода. Свобода - это хорошо',
             'chernomyrdin.txt': 'Хотели как лучше, получилось как всегда',
             'putin.txt': 'Если драка неизбежна, бить нужно первым',
             'orange.txt': 'апельсины лучше, чем картошка. Ешьте апельсины. Они оранжевые',
             'bamnanas.txt': 'Бананы еще вкуснее, чем апельсины. Лучше ешьте бананы вместо апельсинов.'}


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
    out_dict: List[Tuple[str, int]] = []
    for word in re.split('\s+', data.lower()):
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