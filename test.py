from compress import *
from search import *
import pymongo
import pandas as pd
from flask_pymongo import PyMongo

connection = pymongo.MongoClient('127.0.0.1', 27017)
tdb = connection.firstdb
post = tdb.song_poem


def load_or_json(path):
    f = open(path, 'rb')
    reader = json.loads(f.read())
    return reader


def add_docno(reader, docno):
    new_docs = []
    for doc in reader:
        docno += 1
        doc['_id'] = docno
        new_docs.append(doc)
    return new_docs, docno


def add_docno_all(mode):
    file_dictionary = f_dictionary[mode]
    docno_data_p = 'data'# dno_data_p[mode]
    resourece_pathes = os.listdir(file_dictionary)
    docno = 0
    for item in resourece_pathes:
        path = os.path.join(os.getcwd(), '{}\{}'.format(file_dictionary, item))
        if item[0] == 'l':
            add_docno_p = os.path.join(os.getcwd(), '{}\{}'.format(docno_data_p, item))
            f = open(add_docno_p, 'a')
            f.seek(0)
            f.truncate()
            reader = load_or_json(path)
            new_docs, docno = add_docno(reader, docno)
            json.dump(json.dumps(new_docs), f)
            f.close()
        elif item[0] == 'p':
            add_docno_p = os.path.join(os.getcwd(), '{}\{}.json'.format(docno_data_p, item[:-4]))
            f = open(add_docno_p, 'a')
            f.seek(0)
            f.truncate()
            df = pd.read_csv(path, encoding='utf-8', na_values=" NaN").to_json(orient='records')
            reader = json.loads(df)
            new_docs, docno = add_docno(reader, docno)
            json.dump(json.dumps(new_docs), f)
            f.close()


if __name__ == '__main__':
    add_docno_all(2)
    # aaa = [b'(\t\x8d', b'(\t\xa6', b'(\t\xad', b'(\t\xb1', b'(\t\xb8', b'(\t\xbb', b'(\t\xc0', b'(\t\xc1', b'(\t\xc4', b'(\t\xc5', b'(\t\xc7', b'(\t\xc9', b'(\t\xca', b'(\t\xcb', b'(\t\xcc', b'(\t\xcd', b'(\t\xd2', b'(\t\xd7', b'(\t\xd9', b'(\t\xda', b'(\t\xe4', b'(\t\xea', b'(\t\xec', b'(\t\xed', b'(\t\xf1', b'(\t\xf2', b'(\n\x80', b'(\n\x87', b'(\n\x8b', b'(\n\x8e', b'(\n\x91', b'(\n\x94', b'(\n\xad', b'(\n\xae', b'(\n\xb6', b'(\n\xbc', b'(\n\xcd', b'(\n\xce', b'(\n\xd0', b'(\n\xd2', b'(\n\xd6', b'(\n\xd7', b'(\n\xde', b'(\n\xe2', b'(\n\xe3', b'(\n\xee', b'(\n\xef', b'(\n\xf7', b'(\n\xfb', b'(\n\xfc', b'(\n\xfe', b'(\n\xff', b'(\x0b\x82', b'(\x0b\x84', b'(\x0b\x8a', b'(\x0b\x8f', b'(\x0b\x94', b'(\x0b\x95', b'(\x0b\x96', b'(\x0b\x97', b'(\x0b\x98', b'(\x0b\x9a', b'(\x0b\x9c', b'(\x0b\x9e', b'(\x0b\x9f', b'(\x0b\xa2', b'(\x0b\xa3', b'(\x0b\xa4', b'(\x0b\xaa', b'(\x0b\xad', b'(\x0b\xb0', b'(\x0b\xb2', b'(\x0b\xb3', b'(\x0b\xb4', b'(\x0b\xb7', b'(\x0b\xb8', b'(\x0b\xb9', b'(\x0b\xbe', b'(\x0b\xc4', b'(\x0b\xe3', b'(\x0b\xf6', b'(\x0c\x8e', b'(\x0c\x8f', b'(\x0c\x94', b'(\x0c\x98', b'(\x0c\x9f', b'(\x0c\xa2', b'(\x0c\xa6', b'(\x0c\xa7', b'(\x0c\xa9', b'(\x0c\xaf', b'(\x0c\xb0', b'(\x0c\xb2', b'(\x0c\xc6', b'(\x0c\xcc', b'(\x0c\xd0', b'(\x0c\xd4', b'(\x0c\xd5', b'(\x0c\xd6']
    # for item in aaa:
    #     item = decode_vbyte(item)
    #     print(item)
    # search_result = []

    pass
