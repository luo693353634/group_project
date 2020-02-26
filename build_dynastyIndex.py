from config import *
import os
from tools import *
import string
punctuations = string.punctuation


def build_Dynasty_chunk(originFile, dy_index, dyid, dy2id, dyid_p, source='l'):
    nameid_out = open(dyid_p, 'a')
    tmp = dict()
    for doc in originFile:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)
        if source == 'l':
            dynasty = '当代'
        else:  # poem
            if doc['dynasty'] in all_dynasty:
                dynasty = doc['dynasty']
                if dynasty not in tmp.keys():
                    tmp[dynasty] = 1
                else:
                    tmp[dynasty] += 1
            else:
                soted_tmp = sort_dic_value(tmp)
                dynasty = soted_tmp[0][0]
        if dynasty not in dy2id.keys():
            dy2id[dynasty] = dyid
            nameid_out.write(str(dyid) + '\t' + str(dynasty) + '\n')
            dyid += 1

        vb_dyid = encode_vbyte(dy2id[dynasty])
        if vb_dyid not in dy_index.keys():
            dy_index[vb_dyid] = [vb_docno]
        else:
            dy_index[vb_dyid].append(vb_docno)
    return dy_index, dyid, dy2id


def build_dynasty_index(mode):
    did_p = collection_id_p[mode]
    f = open(did_p, 'a')
    f.seek(0)
    f.truncate()

    file_dictionary = docno_dictionary[mode]

    resourece_pathes = os.listdir(file_dictionary)
    dynastyid = 1
    dy2id = {}
    dy_info = {}
    for i, item in enumerate(resourece_pathes):
        print(i, item)
        path = os.path.join(os.getcwd(), '{}/{}'.format(file_dictionary, item))
        reader = load_json(path)
        if item[0] == 'l':
            dy_info, dynastyid, dy2id = build_Dynasty_chunk(reader, dy_info, dynastyid, dy2id, did_p)
        elif item[0] == 'p':
            dy_info, dynastyid, dy2id = build_Dynasty_chunk(reader, dy_info, dynastyid, dy2id, did_p, 'p')
    write_pickle(dy_info, pickle_collectionIndex_p[mode])
    print('finall is {}, write finished'.format(i))
    return dy_info


def write_tokensid_vb(mode):
    tokens_id = load_tokenid(collection_id_p[mode])
    write_pickle(tokens_id, collection_id_vb_p[mode])


dynasty_map = {'秦汉': ['先秦', '秦', '汉', '魏晋', '南北朝'],
               '隋唐': ['隋', '隋末唐初', '唐', '唐末宋初'],
               '宋': ['宋', '宋末元初', '宋末金初', '辽'],
               '元': ['元', '元末明初', '金末元初'],
               '明': ['明', '明末清初'],
               '清': ['清', '清末近现代初', '清末民国初'],
               '当代': ['当代', '民国末当代初', '近现代末当代初', '近现代']}

dynasty_big = ['秦汉', '隋唐', '宋', '元', '明', '清', '当代']
all_dynasty = ['先秦', '秦', '汉', '魏晋', '南北朝', '隋', '隋末唐初', '唐', '唐末宋初', '宋', '宋末元初', '宋末金初', '辽', '元', '元末明初', '金末元初', '明', '明末清初', '清', '清末近现代初', '清末民国初', '当代', '民国末当代初', '近现代末当代初', '近现代']
reversed_dymap = {'先秦': '秦汉', '秦': '秦汉', '汉': '秦汉', '魏晋': '秦汉', '南北朝': '秦汉', '隋': '隋唐', '隋末唐初': '隋唐', '唐': '隋唐', '唐末宋初': '隋唐', '宋': '宋', '宋末元初': '宋', '宋末金初': '宋', '辽': '宋', '元': '元', '元末明初': '元', '金末元初': '元', '明': '明', '明末清初': '明', '清': '清', '清末近现代初': '清', '清末民国初': '清', '当代': '当代', '民国末当代初': '当代', '近现代末当代初': '当代', '近现代': '当代'}


if __name__ == "__main__":
    MODE = mode['product']  # test or product
    terms_info = build_dynasty_index(MODE)
    write_tokensid_vb(MODE)
    print('building index finished')






