# -*- coding=utf-8 -*
import json
import re
import string
import jieba
import operator
import pickle
from preprocess import stopping
from compress import *
import os


def write_pickle(dicc, out_file):
    df2 = open(out_file, 'a')
    df2.seek(0)
    df2.truncate()
    df2.close()
    df2 = open(out_file, 'wb')
    pickle.dump(dicc, df2)
    df2.close()


def write_json(path, dic_w):
    f = open(path, 'a')
    f.seek(0)
    f.truncate()
    json.dump(json.dumps(dic_w), f)
    f.close()


def write_txt(dic_w, path):
    f = open(path, 'wb+')
    f.write(dic_w)
    f.close()


def load_json(path):
    reader = json.loads(json.load(open(path, 'r')))
    # f = open(path, 'r+')
    # reader = json.loads(f.read())
    return reader


def load_pickle(path):
    df = open(path, 'rb')
    reader = pickle.load(df)
    return reader


def load_txt_dic(index_p):
    with open(index_p, 'r') as f:
        return eval(f.read())


def load_tokenid(path='data/token2id'):
    tokens_id = dict()
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.split()
            tokens_id[line[1]] = encode_vbyte(int(line[0]))
    return tokens_id


def load_tokensid_vb(path='data/token2id_vb'):
    tokens_id = (path)
    return tokens_id


def sort_dic_key(dic):
    res = sorted(dic.items(), key=operator.itemgetter(0))
    return res  # format [(0, 1), (2, 1), (5, 1)]


def sort_dic_value(dic):
    res = sorted(dic.items(), key=operator.itemgetter(1))
    if len(res) > 1:
        return reversed(res)  # decreasing
    else:
        return res

if __name__ == '__main__':
    print(sys.getsizeof(encode_vbyte(256)))
    print(sys.getsizeof(256))
    print(sys.getsizeof(bytes(256)))
    print(bytes(256))
    print(encode_vbyte(256))

