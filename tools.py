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


def write_txt(path, dic_w):
    f = open(path, 'a')
    f.seek(0)
    f.truncate()
    f.write(str(dic_w))
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
    return res

def transfer(in_path,out_path):
    index=load_pickle(in_path)
    data=sorted(index.items(),key=lambda x:x[0],reverse=True)
    print(data[0])
    print("read finished")
    new_dict={}
    for i in range(len(data)//2):
        new_dict[data[i][0]]=data[i][1]
    write_pickle(new_dict,out_path)
    print("write finished")
    # json_str=json.dumps(index,skipkeys=True)
    # f=open(out_path,'wb+')
    # f.write(json_str)

if __name__ == '__main__':
        # dicc = {b'\x80': 14, b'\x81': {b'\x81': [1], b'\x86': [213]},
        #         b'\x82': {b'\x81': [2], b'\x8e': [1]}, b'\x83': {b'\x81': [3]},
        #         b'\x84': {b'\x81': [4]}, b'\x85': {b'\x81': [5]},
        #         b'\x86': {b'\x81': [6]}, b'\x87': {b'\x81': [7]},
        #         b'\x88': {b'\x82': [1]}, b'\x89': {b'\x82': [2]},
        #         b'\x8a': {b'\x82': [3]}, b'\x8b': {b'\x83': [1], b'\x84': [1]}, b'\x8c': {b'\x83': [2]},
        #         b'\x8d': {b'\x83': [4, 20, 5]}, b'\x8e': {b'\x83': [5]},
        #         b'\x8f': {b'\x83': [7]}, b'\x90': {b'\x83': [8, 23], b'\x84': [30]},
        #         b'\x91': {b'\x83': [10, 25], b'\x86': [43, 196, 44, 317]},
        #         b'\x92': {b'\x83': [11], b'\x84': [12]}, b'\x93': {b'\x83': [13]}, b'\x94': {b'\x83': [14]},
        #         b'\x95': {b'\x83': [16, 16, 18, 27], b'\x84': [31]},
        #         b'\x96': {b'\x83': [17, 30]}, b'\x97': {b'\x83': [19, 1], b'\x84': [14, 1]},
        #         b'\x98': {b'\x83': [21]}, b'\x99': {b'\x83': [22], b'\x84': [2, 15]},
        #         b'\x9a': {b'\x83': [26], b'\x85': [14], b'\x86': [152, 137, 162, 148, 171, 169, 251, 179], b'\x88': [26]},
        #         b'\x9b': {b'\x83': [27], b'\x84': [5, 17]}, b'\x9c': {b'\x83': [29]}}
        # df2 = open('test.pickle', 'wb')
        # pickle.dump(dicc, df2)
        # df2.close()
        # df = open('test.pickle', 'rb')  # 注意此处是rb
        # # 此处使用的是load(目标文件)
        # data3 = pickle.load(df)
        # print(data3[b'\x9b'])
        transfer("/Users/mac/.ssh/all.index.pickle","/Users/mac/.ssh/new_all.index.pickle")

