
import os
from preprocess import preprocess_query
from config import *
from tools import *
import math
from filterSearch import name_search, dynasty_search
import time
from is_name import get_name_score


# find all docno where the input word occurs
def one_word_search(word, index, token2id):
    res = []
    if word in token2id.keys():
        tokenid = token2id[word]
    else:
        return res
    if tokenid in index.keys():
        for doc in index[tokenid]:
            res.append(doc)
    return res


def multi_words_search(query, index, token2id):
    N = 921771
    doc_score = dict()
    for word in query:
        if word not in token2id.keys():
            continue
        l = len(word)
        res = one_word_search(word, index, token2id)
        df = float(len(res))
        tf = 0
        for docno in res:
            if word in token2id.keys():
                if token2id[word] in index.keys():
                   # tf = float(index[token2id[word]][docno])
                     tf = float(len(index[token2id[word]][docno]))
            w_tfidf = (1 + math.log(tf, 10)) * math.log(N / df, 10)
            if docno not in doc_score.keys():
                doc_score[docno] = w_tfidf * l  # w_tfidf * wordLength
            else:
                doc_score[docno] += w_tfidf * l
    final_res = []
    tmp = sort_dic_value(doc_score)
    for i, item in enumerate(tmp):
        if i < 200:
            final_res.append(item[0])
        else:
            break
    return final_res


def phrase_search(term1, term2, index, token2id):
    res = []
    if term1 not in token2id.keys() or term2 not in token2id.keys():
        return res
    term1 = token2id[term1]
    term2 = token2id[term2]
    if term1 in index.keys() and term2 in index.keys():
        # to reduce running time
        docno_list1 = index[term1] if len(index[term1]) < len(index[term2]) else index[term2]
        docno_list2 = index[term2] if len(index[term1]) < len(index[term2]) else index[term1]
        for docno in docno_list1:
            if docno in docno_list2.keys():  # term1 and term2 in the same doc
                # to reduce running time
                if len(index[term1][docno]) < len(index[term1][docno]):
                    for pos1 in index[term1][docno]:
                        pos2 = int(pos1) + 1
                        if pos2 in index[term2][docno]:
                            res.append(docno)
                            break
                else:
                    for pos2 in index[term2][docno]:
                        pos1 = int(pos2) - 1
                        if pos1 in index[term1][docno]:
                            res.append(docno)
                            break
    return res


def long_phrase_search(phrase, index, token2id):
    res1 = []
    result = []
    for i in range(len(phrase)-1):
        if i == 0:
            res1 = phrase_search(phrase[i], phrase[i+1], index, token2id)
        else:
            res2 = phrase_search(phrase[i], phrase[i+1], index, token2id)
            for item in res2:
                if item in res1:
                    result.append(item)
            res1 = result
            result = []
    return res1


def search_phrase(phrase, index, token2id):
    if len(phrase) == 0:
        return []
    elif len(phrase) == 1:
        res = one_word_search(phrase[0], index, token2id)

    elif len(phrase) == 2:
        res = phrase_search(phrase[0], phrase[1], index, token2id)
    else:
        res = long_phrase_search(phrase, index, token2id)
    return res


# do boolean search for given query
# return the search results (a list of docno)
def search_query(query, index, token2id):
    # analyse the type of query
    if len(query) == 0:
        res = []
    elif len(query) == 1:
        res = one_word_search(query[0], index, token2id)
    else:
        res = multi_words_search(query, index, token2id)
    return res


def final_search(query, phrase, index, nameIndex, collectionIndex,
                 tokens_id, names_id, collection_id,
                 name='', input_big_dynasties=[]):
    result1 = search_phrase(phrase, index, tokens_id)
    result2 = search_query(query, index, tokens_id)  # do boolean search, get a list of doc No

    res_name = name_search(name, nameIndex, names_id)
    print('name_doc: {}'.format(len(res_name)))
    res_d = dynasty_search(input_big_dynasties, collectionIndex, collection_id)
    print('dynastiy_doc: {}'.format(len(res_d)))

    # phrase search
    result = list(set(result1)&set(result2)) + list(set(result1).difference(set(result2)))  # all phrase search result

    # query

    if len(name) and len(input_big_dynasties):
        result = list(set(result) & set(res_name) & set (res_d))
        for docno in result2:
            if docno not in result and docno in res_name and docno in res_d:
                result.append(docno)
    elif len(name):
        result = list(set(result) & set(res_name))
        for docno in result2:
            if docno not in result and docno in res_name:
                result.append(docno)
    elif len(input_big_dynasties):
        result = list(set(result) & set(res_d))
        for docno in result2:
            if docno not in result and docno in res_d:
                result.append(docno)
    else:
        for docno in result2:
            if docno not in result:
                result.append(docno)
    return result


def find_name(query, names_id):
    name_score = dict()
    query = query.split()
    for item in query:
        name_score[item] = get_name_score(item, names_id)
    name_score = sort_dic_value(name_score)
    if name_score[0][1]:
        name = name_score[0][0]
    else:
        name = ''
    return name


if __name__ == '__main__':
    MODE = mode['product']  # test or product
    nameIndex = load_pickle(pickle_singerIndex_p[MODE])  # load singer
    names_id = load_pickle(names_id_vb_p[MODE])
    collectionIndex = load_pickle(pickle_collectionIndex_p[MODE])  # load collection
    collection_id = load_pickle(collection_id_vb_p[MODE])
    query = '李白'
    input_big_dynasties = ['宋', '隋唐']
    name = find_name(query, names_id)
    query, phrase = preprocess_query(query)
    print('phrase: {}'.format(phrase))
    print('query: {}'.format(query))

    # ***********************************************************
    print('begin load')
    print(time.localtime(time.time()))
    index_for_search = load_pickle(pickle_index_p[MODE])  # load index
    tokens_id = load_pickle(tokens_id_vb_p[MODE])
    print('load index finised')
    print(time.localtime(time.time()))
    #***********************************************************

    print('begin search')
    print(time.localtime(time.time()))
    res = final_search(query, phrase, index_for_search, nameIndex, collectionIndex,
                       tokens_id, names_id, collection_id,
                       name, input_big_dynasties)  # get boolean search result

    print('result:')
    for item in res:
        print(decode_vbyte(item))

    print('search finish')
    print(time.time())




