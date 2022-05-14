"""
Вы=исление ранга страницы по ссылкам
"""

from typing import List
import httplib2
from bs4 import BeautifulSoup
from collections import namedtuple

urls: List[str] = ['https://microsoft.com', 'http://oracle.com', 'http://yandex.ru', 'http://google.com']
alpha = 0.15
StaticRank = namedtuple('StaticRank', 'name rank')
static_ranks: List[StaticRank] = [StaticRank(name='Microsoft.com', rank=100),
                                  StaticRank(name='CNN.com', rank=100),
                                  StaticRank(name='RussiaToday.com', rank=100),
                                  StaticRank(name='pupkin.com', rank=1)]


def main():

    mapped_ranks = run_map()

    computed_ranks = run_reduce(mapped_ranks)

    print_ranks(computed_ranks)


def run_map():
    mapped_ranks = {}

    for url in urls:
        links = read_links(url)
        rank = get_static_rank(url)
        for doc_id, rank in map_fn(url, (rank, links)):
            if doc_id not in mapped_ranks.keys():
                mapped_ranks[doc_id] = []
            mapped_ranks[doc_id].append(rank)
    return mapped_ranks


def run_reduce(mapped_ranks):
    computed_ranks = {}

    for doc_id, ranks in mapped_ranks.items():
        rank = reduce_fn(doc_id, ranks)
        computed_ranks[doc_id] = rank

    return computed_ranks


def print_ranks(rank_dict):
    for doc_id, rank in rank_dict.items():
        print(f'{doc_id}: Rank = {rank}')


def get_static_rank(url):
    for doc, rank in static_ranks:
        if doc == url:
            return rank
    return 1


def read_links(url: str) -> List[str]:

    links: List[str] = []

    http = httplib2.Http()
    status, response = http.request(url)

    soup = BeautifulSoup(response, "lxml")

    for link in soup.findAll('a'):
        links.append(link.get('href'))

    return links


def map_fn(k, v):
    rank, outlinks = v
    yield k, 0
    if len(outlinks) > 0:
        for outlink in outlinks:
            yield outlink, float(rank) / len(outlinks)
    else:
        for url in urls:
            yield url, float(rank) / len(urls)


def reduce_fn(k, vs):
    return (1 - alpha) * sum(vs) + alpha / len(urls)


if __name__ == '__main__':
    main()