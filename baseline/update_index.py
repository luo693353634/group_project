# -*- coding=utf-8 -*
from compress import *
from tools import *
import os


def insert_index(index_p, newinfo):
    pre_index = load_txt_dic(index_p) # load index
    tokenid = len(pre_index)+1
    maxdocno = pre_index[encode_vbyte(0)]
    print(maxdocno)


if __name__ == '__main__':
    index_p = '/Users/apple/PycharmProjects/ttds_cw3/test.index'
    newf_info = '酒保将空酒樽收'
    insert_index(index_p, newf_info)
