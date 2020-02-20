# -*- coding=utf-8 -*
import pandas as pd
from config import *
from tools import *
punctuations = string.punctuation


def build_chunk_lyrics(reader, terms_info, tokenid, token2id, tid_p):
    tid_out = open(tid_p, 'a')
    flag = 1
    for doc in reader:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        content = doc['lyric']
        content = re.sub(r'\[[0-9]{2}:[0-9]{2}\.[0-9]{2,}]', '', content)
        content = re.sub(r'[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+', ' ', content)
        # 这里加上歌手名字不分词的操作
        #**********code*********#
        content = jieba.lcut_for_search(content)
        content = stopping(content)
        if flag:
            print(content)
            flag = 0

        for i, token in enumerate(content):  # 有些空格会算一个词，在这里保留占位
            if len(token.strip()):  # not space
                # add token to t2id dictionary
                if token not in token2id.keys():
                    token2id[token] = tokenid
                    tid_out.write(str(tokenid) + '\t' + token + '\n')
                    tokenid += 1

                vb_tokenid = encode_vbyte(token2id[token])  # compress token id
                if vb_tokenid not in terms_info.keys():  # new term
                    terms_info[vb_tokenid] = {vb_docno: [i + 1]}  # first pos in a doc
                else:  # exist term
                    if vb_docno not in terms_info[vb_tokenid].keys():  # new doc for this term
                        terms_info[vb_tokenid][vb_docno] = [i + 1]
                    else:  # exist term, exist doc
                        terms_info[vb_tokenid][vb_docno].append(
                                i + 1 - terms_info[vb_tokenid][vb_docno][-1])  # delta encoded position
    return terms_info, tokenid, token2id


def build_chunk_poem(df, terms_info, tokenid, token2id, tid_p):
    tid_out = open(tid_p, 'a')
    flag = 1
    for doc in df:
        docno = doc['_id']
        vb_docno = encode_vbyte(docno)

        content = doc['content']
        if content is None:
            continue
        content = re.sub(r'\[[0-9]{2}:[0-9]{2}\.[0-9]{2,}]', '', content)
        content = re.sub(r'[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+', ' ', content)
        tmp = content
        content = jieba.lcut_for_search(content)
        content = stopping(content)
        for word in tmp:  # 添加单字分词逻辑
            content.append(word)

        if flag:
            print(content)
            flag = 0

        for i, token in enumerate(content):  # 有些空格会算一个词，在这里保留占位
            if len(token.strip()):  # not space
                # add token to t2id dictionary
                if token not in token2id.keys():
                    token2id[token] = tokenid
                    tid_out.write(str(tokenid) + '\t' + token + '\n')
                    tokenid += 1
                vb_tokenid = encode_vbyte(token2id[token])  # compress token id

                if vb_tokenid not in terms_info.keys():  # new term
                    terms_info[vb_tokenid] = {vb_docno: [i + 1]} # first pos in a doc
                else:  # exist term
                    if vb_docno not in terms_info[vb_tokenid].keys():  # new doc for this term
                        terms_info[vb_tokenid][vb_docno] = [i + 1]
                    else:  # exist term, exist doc
                        terms_info[vb_tokenid][vb_docno].append(
                                i + 1 - terms_info[vb_tokenid][vb_docno][-1])  # delta encoded position
    return terms_info, tokenid, token2id


def write_index_for_view(tinfo, out_path):
    tinfo = sorted(tinfo.items(), key=operator.itemgetter(0))
    with open(out_path+'.view', 'a') as f:
        f.seek(0)
        f.truncate()
        for tinfo_item in tinfo:
            if tinfo_item[0] == encode_vbyte(0):
                f.write('maxdocno is {}\n'.format(tinfo_item[1]))
                continue
            f.write(str(tinfo_item[0]) + ':')  # term
            df = len(tinfo_item[1])  # df
            f.write('('+str(df)+')\n')
            # doc
            doc_info = tinfo_item[1]
            doc_info = sorted(doc_info.items(), key=operator.itemgetter(0))
            for item in doc_info:
                # docno
                f.write('\t'+str(item[0]))
                f.write(':')
                # tf
                tf = len(item[1])
                f.write('('+str(tf)+') ')
                # term position
                for i, position in enumerate(item[1]):
                    f.write(str(position))
                    if i < tf-1:
                        f.write(',')
                f.write('\n')
            f.write('\n')
        f.close()
    return


def build_index(mode):
    file_dictionary = docno_dictionary[mode]

    tid_p = tokens_id_p[mode]
    f = open(tid_p, 'a')
    f.seek(0)
    f.truncate()

    tokenid = 1
    token2id = dict()
    terms_info = dict()
    resourece_pathes = os.listdir(file_dictionary)
    for i, item in enumerate(resourece_pathes):
        print(i, item)
        path = os.path.join(os.getcwd(), '{}/{}'.format(file_dictionary, item))
        reader = load_json(path)
        if item[0] == 'l':
            terms_info, tokenid, token2id = build_chunk_lyrics(reader, terms_info, tokenid, token2id, tid_p)
        elif item[0] == 'p':
            terms_info, tokenid, token2id = build_chunk_poem(reader, terms_info, tokenid, token2id, tid_p)
    write_pickle(terms_info, pickle_index_p[MODE])
    write_index_for_view(terms_info, txt_index_p[MODE])
    print('finall is {}, write finished'.format(i))
    return terms_info


def add_docno(reader, docno):
    new_docs = []
    for doc in reader:
        docno += 1
        doc['doc_id'] = docno
        new_docs.append(doc)
    return new_docs, docno


def add_docno_all(mode):
    file_dictionary = f_dictionary[mode]
    docno_data_p = dno_data_p[mode]
    resourece_pathes = os.listdir(file_dictionary)
    docno = 0
    for item in resourece_pathes:
        path = os.path.join(os.getcwd(), '{}/{}'.format(file_dictionary, item))
        if item[0] == 'l':
            add_docno_p = os.path.join(os.getcwd(), '{}/{}'.format(docno_data_p, item))
            f = open(add_docno_p, 'a')
            f.seek(0)
            f.truncate()
            reader = load_json(path)
            new_docs, docno = add_docno(reader, docno)
            json.dump(json.dumps(new_docs), f)
            f.close()
        elif item[0] == 'p':
            add_docno_p = os.path.join(os.getcwd(), '{}/{}.json'.format(docno_data_p, item[:-4]))
            f = open(add_docno_p, 'a')
            f.seek(0)
            f.truncate()
            df = pd.read_csv(path, encoding='utf-8', na_values=" NaN").to_json(orient='records')
            reader = json.loads(df)
            new_docs, docno = add_docno(reader, docno)
            json.dump(json.dumps(new_docs), f)
            f.close()


def write_tokensid_vb(mode):
    tokens_id = load_tokenid(tokens_id_p[mode])
    write_pickle(tokens_id, tokens_id_vb_p[mode])


if __name__ == '__main__':
    MODE = mode['product']  # test or product
    #add_docno_all(MODE)
    terms_info = build_index(MODE)
    write_tokensid_vb(MODE)
    print('building index finished')

    # df = open(pickle_index_p[MODE], 'rb')  # 注意此处是rb
    # # 此处使用的是load(目标文件)
    # data3 = pickle.load(df)
    # print(data3)
    # df = open(tokens_id_vb_p[MODE], 'rb')  # 注意此处是rb
    # # 此处使用的是load(目标文件)
    # data3 = pickle.load(df)
    # print(data3)





