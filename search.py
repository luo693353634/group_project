# -*- coding=utf-8 -*
import os
from preprocess import preprocess_query
from config import *
from tools import *
import math

# get all docno in the index, return a list of docno
def get_all_doc(index):
    res = []
    for term in index:
        for doc in index[term].keys():
            if doc not in res:
                res.append(doc)
    return res


# AND search
# for given term1, term2, index,
# return a list containing all docno where both term1 and term2 occur
def and_search(term1, term2, index):
    res = []
    term1 = encode_vbyte(term1)
    term2 = encode_vbyte(term2)
    if term1 in index.keys() and term2 in index.keys():
        if len(index[term1]) < len(index[term2]):
            for item in index[term1]:
                if item in index[term2].keys():
                    res.append(item)
        else:
            for item in index[term2]:
                if item in index[term1].keys():
                    res.append(item)
    return res


# OR search
# for given term1, term2, index,
# return a list containing all docno where both term1 or term2 occur
def or_search(term1, term2, index):
    res = []
    if term1 in index.keys() and term2 in index.keys():
        if len(index[term1]) < len(index[term2]):
            res = index[term2].keys()
            for docno in index[term1]:
                if docno not in res:
                    res.append(docno)
        else:
            res = index[term1].keys()
            for docno in index[term1]:
                if docno not in res:
                    res.append(docno)
    return res


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
    N = 3
    doc_score = dict()
    res = []
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
                    tf = float(len(index[token2id[word]][docno]))
            w_tfidf = (1 + math.log(tf, 10)) * math.log(N / df, 10)
            if docno not in doc_score.keys():
                doc_score[docno] = w_tfidf * l  # w_tfidf * wordLength
            else:
                doc_score[docno] += w_tfidf * l
    for item in sort_dic_value(doc_score):
        res.append(item[0])
    return res


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


def search(query, phrase, index, tokens_id):
    result1 = search_phrase(phrase, index, tokens_id)
    result2 = search_query(query, index, tokens_id)  # do boolean search, get a list of doc No

    result = []
    tmp = []
    # phrase search
    for docno in result1:
        if docno in result2:  # in both phrase and query
            result.append(docno)
        else:
            tmp.append(docno)
    result = result + tmp  # all phrase search result

    # query
    for docno in result2:
        if docno not in result:
            result.append(docno)
    return result


if __name__ == '__main__':
    MODE = mode['test']  # test or product

    index_for_search = load_pickle(pickle_index_p[MODE])  # load index
    tokens_id = load_pickle(tokens_id_vb_p[MODE])

    query1 = '北京\'花草\''
    query2 = '天安门'
    query3 = '郑楠'
    query4 = '花儿\'太阳当空照\''
    query, phrase = preprocess_query(query2)
    res = search(query, phrase, index_for_search, tokens_id)  # get boolean search result
    print('result:')
    if len(res) > 20:
        res = (res[:20])
    else:
        res = (res)
    for item in res:
        print(decode_vbyte(item))
