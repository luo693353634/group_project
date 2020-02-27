from config import *
import os
from tools import *


def build_singer(originFile, n_index, nid, n2id, nameid_p):
    nameid_out = open(nameid_p, 'a')
    for doc in originFile:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        singer = doc['artist_name']
        if singer not in n2id.keys():
            n2id[singer] = nid
            nameid_out.write(str(nid) + '\t' + singer + '\n')
            nid += 1

        vb_nid = encode_vbyte(n2id[singer])  # compress name id
        if vb_nid not in n_index.keys():  # new name
            n_index[vb_nid] = [vb_docno]
        elif vb_docno not in n_index[vb_nid]:
            n_index[vb_nid].append(vb_docno)
    return n_index, nid, n2id


def build_poet(originFile, n_index, nid, n2id, nameid_p):
    nameid_out = open(nameid_p, 'a')
    for doc in originFile:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        poet = doc['author']
        if poet not in n2id.keys():
            n2id[poet] = nid
            nameid_out.write(str(nid) + '\t' + str(poet) + '\n')
            nid += 1

        vb_nid = encode_vbyte(n2id[poet])  # compress name id
        if vb_nid not in n_index.keys():  # new name
            n_index[vb_nid] = [vb_docno]
        elif vb_docno not in n_index[vb_nid]:
            n_index[vb_nid].append(vb_docno)
    return n_index, nid, n2id


def build_index(mode):
    nid_p = names_id_p[mode]
    f = open(nid_p, 'a')
    f.seek(0)
    f.truncate()

    file_dictionary = docno_dictionary[mode]

    resourece_pathes = os.listdir(file_dictionary)
    name_id = 1
    name2id = {}
    names_info = {}
    for i, item in enumerate(resourece_pathes):
        print(i, item)
        path = os.path.join(os.getcwd(), '{}/{}'.format(file_dictionary, item))
        reader = load_json(path)
        if item[0] == 'l':
            names_info, name_id, name2id = build_singer(reader, names_info, name_id, name2id, nid_p)
        elif item[0] == 'p':
            names_info, name_id, name2id = build_poet(reader, names_info, name_id, name2id, nid_p)
    write_pickle(names_info, pickle_singerIndex_p[mode])
    print('finall is {}, write finished'.format(i))
    return names_info


def write_namesid_vb(mode):
    names_id = load_tokenid(names_id_p[mode])
    write_pickle(names_id, names_id_vb_p[mode])


if __name__ == "__main__":
    MODE = mode['product']  # test or product
    terms_info = build_index(MODE)
    write_namesid_vb(MODE)
    print('building index finished')
