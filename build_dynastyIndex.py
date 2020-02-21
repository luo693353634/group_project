from config import *
import os
from tools import *


def build_albumn(originFile, n_index, nid, n2id, nameid_p):
    nameid_out = open(nameid_p, 'a')
    for doc in originFile:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        singer = doc['album_name']
        if singer not in n2id.keys():
            n2id[singer] = nid
            nameid_out.write(str(nid) + '\t' + singer + '\n')
            nid += 1

        vb_nid = encode_vbyte(n2id[singer])  # compress name id
        if vb_nid not in n_index.keys():  # new name
            n_index[vb_nid] = [vb_docno]
            # n_index[vb_nid] = [docno]
        elif vb_docno not in n_index[vb_nid]:
            n_index[vb_nid].append(vb_docno)
            # n_index[vb_nid].append(docno)
    return n_index, nid, n2id


def build_poemDynasty(originFile, n_index, nid, n2id, nameid_p):
    nameid_out = open(nameid_p, 'a')
    for doc in originFile:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        poet = doc['dynasty']
        if poet not in n2id.keys():
            n2id[poet] = nid
            nameid_out.write(str(nid) + '\t' + str(poet) + '\n')
            nid += 1

        vb_nid = encode_vbyte(n2id[poet])  # compress name id
        if vb_nid not in n_index.keys():  # new name
            n_index[vb_nid] = [vb_docno]
            # n_index[vb_nid] = [docno]
        elif vb_docno not in n_index[vb_nid]:
            n_index[vb_nid].append(vb_docno)
            # n_index[vb_nid].append(docno)
    return n_index, nid, n2id


def build_index(mode):
    nid_p = collection_id_p[mode]
    f = open(nid_p, 'a')
    f.seek(0)
    f.truncate()

    file_dictionary = docno_dictionary[mode]

    resourece_pathes = os.listdir(file_dictionary)
    collection_id = 1
    collection2id = {}
    collection_info = {}
    for i, item in enumerate(resourece_pathes):
        print(i, item)
        path = os.path.join(os.getcwd(), '{}/{}'.format(file_dictionary, item))
        reader = load_json(path)
        if item[0] == 'l':
            collection_info, collection_id, collection2id = build_albumn(reader, collection_info, collection_id, collection2id, nid_p)
        elif item[0] == 'p':
            collection_info, collection_id, collection2id = build_poemDynasty(reader, collection_info, collection_id, collection2id, nid_p)
    write_pickle(collection_info, pickle_collectionIndex_p[mode])
    write_index_for_view(collection_info, txt_collectionIndex_p[mode])
    print('finall is {}, write finished'.format(i))
    return collection_info


def write_index_for_view(tinfo, out_path):
    tinfo = sorted(tinfo.items(), key=operator.itemgetter(0))
    with open(out_path+'.view', 'a') as f:
        f.seek(0)
        f.truncate()
        for tinfo_item in tinfo:
            if tinfo_item[0] == encode_vbyte(0):
                f.write('maxdocno is {}\n'.format(tinfo_item[1]))
                continue
            f.write(str(decode_vbyte(tinfo_item[0])) + ':')  # name_vbyte_id
            df = len(tinfo_item[1])  # df
            f.write('('+str(df)+')\n')
            # doc
            doc_info = tinfo_item[1]
            for doc in doc_info:
                f.write('\t'+str(decode_vbyte(doc)))
            f.write('\n')
    return


def write_tokensid_vb(mode):
    tokens_id = load_tokenid(collection_id_p[mode])
    write_pickle(tokens_id, collection_id_vb_p[mode])


if __name__ == "__main__":
    MODE = mode['product']  # test or product
    terms_info = build_index(MODE)
    write_tokensid_vb(MODE)
    print('building index finished')
