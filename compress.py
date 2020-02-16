# -*- coding=utf-8 -*
from struct import pack, unpack
import sys


def encode_vbyte(number):
    """Variable byte code encode number.
    Usage:
      import vbcode
      vbcode.encode_number(128)
    """
    bytes_list = []
    while True:
        bytes_list.insert(0, number % 128)
        if number < 128:
            break
        number = number // 128
    bytes_list[-1] += 128
    return pack('%dB' % len(bytes_list), *bytes_list)


def decode_vbyte(bytestream):
    """Variable byte code decode.
    Usage:
      import vbcode
      vbcode.decode(bytestream)
        -> [32, 64, 128]
    """
    n = 0
    numbers = 0
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers += n
            n = 0
    return numbers


def decode_delta(delta_list):
    ori_list = []
    for ele in delta_list:
        if len(ori_list) == 0:
            ori_list.append(ele)
        else:
            ori_list.append(ele + ori_list[-1])
    return ori_list


def decode_index(ori_index, token_path):
    f = open(token_path, 'r')
    # preprocess token.txt
    tokens = {}
    for line in f.readlines():
        tmp = line.split()
        tokens[int(tmp[0])] = tmp[1]
    new_index = {}
    for key1 in ori_index.keys():
        new_index[tokens[decode_vbyte(key1)]] = {}
        for key2 in ori_index[key1].keys():
            new_index[tokens[decode_vbyte(key1)]][decode_vbyte(key2)] = decode_delta(ori_index[key1][key2])
    return new_index

