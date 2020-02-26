# -*- coding=utf-8 -*
from config import *
from tools import *
from build_dynastyIndex import *


def most_similar(name):
    name_list = [name]

    return name_list


def dynasty_search(input_big_dynasties, cIndex, cid):
    res = []
    flag = 1
    dynasties = []
    for item in input_big_dynasties:
        dynasties = set(dynasties)| set(dynasty_map[item])
    for item in dynasties:
        dynasty_id = cid[item]
        if flag:
            res = set(cIndex[dynasty_id])
            flag = 0
        else:
            res = res|set(cIndex[dynasty_id])
    return list(res)


def name_search(name, nIndex, nid):
    if len(name) == 0:
        return []
    res = []
    standard_names = most_similar(name)
    for item in standard_names:
        name_id = nid[item]
        for docno in nIndex[name_id]:
            if docno not in res:
                res.append(docno)
    return res


def filter_search(name, input_big_dynasties, nIndex, cIndex, nid, cid):
    res1 = name_search(name, nIndex, nid)
    print(len(res1))
    res2 = dynasty_search(input_big_dynasties, cIndex, cid)  # do boolean search, get a list of doc No
    res = set(res1) & set(res2)
    return res


if __name__ == '__main__':
    MODE = mode['product']  # test or product

    nameIndex = load_pickle(pickle_singerIndex_p[MODE])  # load singer
    names_id = load_pickle(names_id_vb_p[MODE])
    collectionIndex = load_pickle(pickle_collectionIndex_p[MODE])  # load collection
    collection_id = load_pickle(collection_id_vb_p[MODE])


    name = '李白'
    input_big_dynasties = []
    res1 = name_search(name, nameIndex, names_id)
    print(len(res1))
    res2 = dynasty_search(input_big_dynasties, collectionIndex, collection_id)  # do boolean search, get a list of doc No
    print(len(res2))


    #filter_res = filter_search(name, input_big_dynasties, nameIndex, collectionIndex, names_id, collection_id)
    #print(len(filter_res))
