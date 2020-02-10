import xml.etree.ElementTree as ET
import nltk
from nltk.corpus import stopwords
import re
import json
import math

def dict_read(name):        #Read dictionary(json file)
    f = open(name, "r")
    dict = json.load(fp=f)
    return dict

def tf_idf(text):
    queries=[]
    index=dict_read("dict1 2.json")
    line=preprocess(text)
    queries.append(line)
    weight={}
    number = len(xml_read("trec.5000 2.xml", "DOCNO"))
    for i in range(len(queries)):
        query=queries[i]
        for word in query:
            if word not in weight:
                position=index[word]
                df=len(position)
                id_score=[]
                for j in range(df):
                    id=position[j][0]
                    link=re.findall(r"\w+",position[j][1])
                    tf=len(link)
                    w=(1+math.log10(tf))*math.log10(number/df)
                    if w!=0:
                        id_score.append([id,w])
                weight[word]=id_score
        score={}
        for word in query:
            id_word_weight=weight[word]
            for j in range(len(id_word_weight)):
                if id_word_weight[j][0] not in score:
                    score[id_word_weight[j][0]]=id_word_weight[j][1]
                else:
                    score[id_word_weight[j][0]]+=id_word_weight[j][1]
        rank=sorted(score.items(),key=lambda item:item[1],reverse=True)[:20]
        result=[]
        """
        这里通过倒排索引找到了文本的唯一编码，需要通过反向检索，通过查找唯一索引来找到文章的具体内容和标题
        """
        for name in rank:
            result.append(xml_research(name[0]))#如果用XML解析的办法非常慢，这里用的XML解析
        print(result)
        return result

def preprocess(text):        #Preprocess the text
    lower = text.lower()  # translate to lower
    tokens=re.sub(r'\w+\'[t]','',lower)  #delete word with (n't), e.g didn't
    '''
    tokens = re.findall(r'\w+[-\w+]*', tokens)
    
    This line is to split word with "-", however, I don't think it is useful. Even though I delete "-"
    between the word, the meaning of the word and the topic will not change.
    '''
    tokens=re.findall(r'\w+',tokens)      #Split the word without special treatment
    stop_words = stopwords.words("english")# stopwords documents
    filtered_tokens = []
    for w in tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    s = nltk.stem.SnowballStemmer("english")
    normalisation_tokens = [s.stem(ws) for ws in filtered_tokens]
    return normalisation_tokens     #Output is a list

def xml_read(name, tag):    #Read xml file
    tree = ET.parse(name)
    lines = []
    for elem in tree.iter(tag):
        lines.append(elem.text)
    return lines

"""
这是XML解析的办法，但是因为速度太慢，建议改成SQL注入。如果是SQL的话，建议使用面向对象的方法
先定义属性，例如标题，作者，正文内容等等。
"""
def xml_research(text):
    tree=ET.parse("trec.5000 2.xml")
    for elem in tree.iter("DOC"):
        if elem.find("DOCNO").text==text:
            title=elem.find("HEADLINE").text
            return title

