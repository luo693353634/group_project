# -*- coding=utf-8 -*
import re
import jieba
import sys
import json
import os
import operator


def tokenlization_conntent(strr):
    jieba.add_word('制作人')
    # delete time target
    strr = re.sub(r'\[[0-9]{2}:[0-9]{2}\.[0-9]{2,}]', '', strr)
    strr = re.sub(r'[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+', '', strr)
    strr = re.compile(r'(\/\w+)|(\d+\-\S+)|(\[)|(\]\S+)').sub('', strr)
    res = jieba.lcut_for_search(strr)
    return res


def stopping(line_tokens):
    with open('data/stopwords.txt', 'r', encoding='UTF-8') as f:
        stw_list = []
        for stw in f.readlines():
            stw_list.append(stw.strip())
    for i, item in enumerate(line_tokens):
        if item in stw_list:
            line_tokens.pop(i)
    return line_tokens


def preprocess_CN(line):
    token_list = tokenlization_conntent(line)
    pure_token_list = stopping(token_list)
    return pure_token_list


def preprocess_query(query):
    begin = -1
    end = -1
    flag = 0
    phrase = []
    for i, item in enumerate(query):
        if item == '\'' and begin == -1:
            begin = i
        elif item == '\'':
            end = i
            flag = 1
            break
        elif item == '\"' and begin == -1:
            begin = i
        elif item == '\"':
            flag = 1
            end = i
            break
    if flag:
        phrase = jieba.lcut_for_search(query[begin+1:end])

    res = jieba.lcut_for_search(query)
    for item in query:
        res.append(item)
    res = stopping(res)
    return res[:20], phrase


def preprocess_sname(sn):  # 歌名提纯
    sn = re.sub(u"\\（.*?\\）|\(.*?\)|\[.*?\]", "", sn)
    if '-' in sn:
        res = sn.split('-')
        return res[1]
    else:
        return sn


def load_data(N):
    song_names = []
    artists = []
    for i in range(1, N, 1):
        path = os.path.join(os.getcwd(), 'resources/lyric_part{}.json'.format(i))
        with open(path, 'r') as f:
            reader = json.loads(f.read())
            for item in reader:
                sn = preprocess_sname(item['song_name'])
                if sn not in song_names:
                    song_names.append(sn)
                if item['artist_name'] not in artists:
                    artists.append(item['artist_name'])
    return song_names, artists


def fetch_vocabulary(N):
    vocabulary = dict()
    count = 0
    for i in range(1, N, 1):
        path = os.path.join(os.getcwd(), 'resource/lyric_part{}.json'.format(i))
        with open(path, 'r') as f:
            reader = json.loads(f.read())
            for item in reader:
                token_list = preprocess_CN(item['lyric'])
                for word in token_list:
                    if word not in vocabulary:
                        vocabulary[count] = word
                        count += 1
    return vocabulary


def write_sns(song_names):
    path = os.path.join(os.getcwd(), 'data/song_names')
    with open(path, 'w') as f:
        for item in song_names:
            f.write(item)
            f.write('\n')
        f.close()


def write_artists(artists):
    path = os.path.join(os.getcwd(), 'data/artists')
    with open(path, 'w') as f:
        for item in artists:
            f.write(item)
            f.write('\n')
        f.close()


# def write_vocabulary(vocabulary):
#     sorted_vol = sorted(vocabulary.items(), key=operator.itemgetter(0))
#     with open(os.path.join(os.getcwd(), 'data/dictionary'), 'w') as f:
#         for item in sorted_vol:
#             f.write(str(item[0]))
#             f.write('\t:\t')
#             f.write(item[1])
#             f.write('\n')


if __name__ == '__main__':
    song_names, artists = load_data(2)
    write_artists(artists)
    write_sns(song_names)
    # volcabulary = fetch_vocabulary(14)
    #write_vocabulary(volcabulary)

