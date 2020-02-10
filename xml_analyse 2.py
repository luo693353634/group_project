import xml.etree.ElementTree as ET
import nltk
import re
import json
import codecs
import math
'''
Before you use this program to create new file. Please make sure you have changed the name
or you can delete the old file.

The name of different output has written in the end of this code.

If you don't know the meaning of parameter, you can check the notes before function. There are some details
about the parameter and output. There are also some notes to describe the key process.

I have trained this model, so I read inverted index directly. There are some important document:
"dict.json" is a dictionary for inverted index  
"index.txt" is the output for inverted index
"queries.boolean.txt" is the result for boolean search
"result.ranked.txt" is the result for retrieval.
'''
def text_read(name):        #Read stopwords document(txt)
    f = open(name, "r")
    text = f.read()
    f.close()
    return text

def xml_read(name, tag):    #Read xml file
    tree = ET.parse(name)
    lines = []
    for elem in tree.iter(tag):
        lines.append(elem.text)
    return lines            #output is a list

def dict_read(name):        #Read dictionary(json file)
    f = open(name, "r")
    dict = json.load(fp=f)
    return dict

def dict_write(name, dict):  #Write dictionary(json file)
    outf = codecs.open(name, "a", "utf-8")
    json.dump(dict, outf, ensure_ascii=False)

def write(word, name):        #Write into a file（txt）
    f = open(name, "a")
    f.write(word + "\n")
    f.close()
"""
parameter "dict" is a dictionary, "name" is the name for output file
"""
def print_index(dict,name):    #Output inverted_index into a file
    index=sorted(dict.items())
    for i in range(len(index)):
        write(index[i][0]+":",name)
        position=index[i][1]
        for j in range(len(position)):
            write("\t"+position[j][0]+": "+",".join(position[j][1:]),name)
"""
parameter "q_id" is number, "answer" is a list,"name" is the name for output file
"""
def print_boolean(q_id,answer,name):   #Output boolean research result
    for id in answer:
        write(str(q_id)+" 0"+" "+str(id)+" 0"+" 1"+" 0" ,name)
"""
parameter "q_id" is number, "rank" is a list,"name" is the name for output file
"""
def print_ranked(q_id,rank,name):      #Output ranked retrieval result
    for i in range(len(rank)):
        write(str(q_id)+" 0"+" "+str(rank[i][0])+" 0"+" "+str(rank[i][1])[:6]+" 0" ,name)

"""
The parameter "text" is String
The output for this function is a list.
"""
def preprocess(text):        #Preprocess the text
    lower = text.lower()  # translate to lower
    tokens=re.sub(r'\w+\'[t]','',lower)  #delete word with (n't), e.g didn't
    '''
    tokens = re.findall(r'\w+[-\w+]*', tokens)
    
    This line is to split word with "-", however, I don't think it is useful. Even though I delete "-"
    between the word, the meaning of the word and the topic will not change.
    '''
    tokens=re.findall(r'\w+',tokens)      #Split the word without special treatment
    stop_words = text_read("englishST.txt").split()  # stopwords documents
    filtered_tokens = []
    for w in tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    s = nltk.stem.SnowballStemmer("english")
    normalisation_tokens = [s.stem(ws) for ws in filtered_tokens]
    return normalisation_tokens     #Output is a list

"""
This function is to get the inverted_index. 
Parameter "name" is the name for corpus document, which is a xml.
The output for this function is a dict
"""
def get_index(name):         #Create inverted_index
    titles = xml_read(name, "HEADLINE")
    len_titles = []          #Store the length of headline for each ID
    lines = xml_read(name, "TEXT")
    seq = []                 #Seq store the text after preprocessing
    for i in range(len(titles)):
        title = preprocess(titles[i])
        tokens = preprocess(lines[i])
        len_titles.append(str(len(title)))
        tokens = title + tokens     #Combine headline and text
        seq.append(tokens)
    id = xml_read(name, "DOCNO")   #Store article ID
    headline_value = []     #The link for headline
    for i in range(len(id)):
        headline_value.append([id[i], "1:" + len_titles[i]])
    whole_seq = []         #Store the whole word appear in corpus
    for i in range(len(seq)):
        for word in seq[i]:
            if word not in whole_seq:
                whole_seq.append(word)
    dict = {}    #This dictionary is to match article's id and its text
    for k in range(len(id)):
        dict[id[k]] = seq[k]
    index = {}  #This dictionary store inverted_index
    for word in whole_seq: #Words in this list are unique
        position = []   # store position and article ID, like [ID,position]
        for i in dict.keys(): #Find in one article
            link = []     #This list is to store position for a word in a document
            for j in range(len(dict[i])):
                if word == dict[i][j]: #Find the position j in article i
                    link.append(str(j + 1)) # j begins from 0
            if len(link) != 0:
                position.append([i, ",".join(link)]) # match position and article ID
        index[word] = position #Write into dictionary. e.g {word: ["1","2,3,4"]}
        print(position)
    index["headline"] = headline_value  #Write link for headline
    return index       #Output is a dict

"""
This function implement boolean research and proximity search
Parameter "name" is the question ducument(txt). "index" means inverted index(dict) that I build before.
    "Output" is the file which I write results into.
"""
def research(name, index,output):
    f = open(name, "r")
    lines = f.readlines()
    questions = []
    for question in lines:
        questions.append(question.strip())  #read questions and store into list
    for i in range(len(questions)):
        question = re.sub(r"^\w+\s","",questions[i]) #remove quetion id like "1 "
        if "#" in question:                            # "#" means proximity search
            pattern = re.compile(r"^#[0-9]+")
            proximity = re.findall(pattern, question)
            number = int(proximity[0][1:])            #get the distance limitation
            pattern = re.compile(r"\w+\,\s*\w+")      #match two words like "a,b" without other character
            word = re.findall(pattern, question)[0]
            word = re.split(r"\W+", word)             #split and get a list
            word1 = preprocess(word[0])[0]    #word1 and word2 are str not list
            word2 = preprocess(word[1])[0]
            result=get_proximity(word1,word2,index,number,True)
            print_boolean(i+1,result,output)
        else:
            if "\"" in question:            #word with " will use different method to handle
                number=1
                pattern = re.compile(r"\"\w+\s\w+\"")
                word = re.findall(pattern, question)
                if len(word)==1:       #only have one phrase, another one is word
                    word1=word[0].split() #find word "word1 word2" and get list [word1,word2]
                    word2 = re.sub(pattern, "", question).split()    #only keep another part,and get list[word3, word4,...]
                    word1_1=preprocess(word1[0])[0]
                    word1_2=preprocess(word1[1])[0]
                    list1=get_proximity(word1_1,word1_2,index,number,False) #return the result for "word1"
                    result=get_id(list1,word2,index)
                    print_boolean(i+1,result,output)
                else:           #both of two words are phrases
                    result=[]
                    word1=word[0].split()
                    word2=word[1].split()
                    word1_1,word1_2=preprocess(word1[0])[0],preprocess(word1[1])[0]
                    word2_1,word2_2=preprocess(word2[0])[0],preprocess(word2[1])[0]
                    list1=get_proximity(word1_1,word1_2,index,number,False)#return the result for "word1"
                    list2=get_proximity(word2_1,word2_2,index,number,False)#return the result for "word2"
                    word2 = re.sub(pattern, "", question).split()
                    if "AND" in word2:          #if the logic connection is "AND"
                        if "NOT" in word2:      #if "NOT" for phrase2
                            for a in list1:
                                if a not in list2:
                                    result.append(a)
                        else:
                            for a in list1:
                                if a in list2:
                                    result.append(a)
                    if "OR" in word2:           #if the logic connection is "OR"
                         for a in list1:
                            result.append(a)
                         for b in list2 :
                            if b not in result:
                                result.append(b)
                         result=map(int,result)  #change string to int for each element.
                         result=sorted(result)   #sorting
                         result=[str(i) for i in result] #make sure document_id is string.
                    print_boolean(i+1,result,output)
            else:
                word = re.findall("\w+", question) #separate the word
                word1 = word[0]
                word1 = preprocess(word1)[0]
                word2 = word[1:]
                list1=get_list(word1,index) # the result for word1
                result=get_id(list1,word2,index)
                print_boolean(i+1,result,output)
'''
This function is to get the documents' id with word1
Parameter "word1" is a word, "index" is inverted index, a dictionary
Output for this function is a list
'''
def get_list(word1,index):
    list=index[word1]
    list1=[]
    for i in range(len(list)):
        if list[i][0] not in list1:
            list1.append(list[i][0])
    return list1
'''
This function is to get results for proximity research
Parameter "word1" and "word2" are words(String), "index" is inverted index, a dictionary
"number" is the distance between two words.
Output for this function is a list
'''
def get_proximity(word1,word2,index,number,absolute_value):
    document=[]
    list1=index[word1]
    list2=index[word2]
    for a in list1:
        for b in list2:
            if a[0]==b[0]: #have same ID
                a_positions=re.findall(r"\w+",str(a[1]))    #The position for list1
                b_positions=re.findall(r"\w+",str(b[1]))    #The position for list2
                for a_position in a_positions:  #choose one position
                    for b_position in b_positions:  #choose one position
                        if absolute_value==True:
                            if abs(int(a_position)-int(b_position))<=number and a[0] not in document:
                                document.append(a[0])      #This is for proximity search
                        elif absolute_value==False:
                            if int(b_position)-int(a_position)==number and a[0] not in document:
                                document.append(a[0])       #This is for phrase and consider the order
    return document
'''
This function is to get results for boolean research
Parameter "word1" is a word, index is inverted index, a dictionary
Output for this function is a list
'''
def get_id(list1, word2, index):
    document=[]
    if "AND" in word2:          #if "AND" in word2
        word2.remove("AND")
        if "NOT" in word2:      #if "NOT" in word2
            word2.remove("NOT")
            word2 = preprocess(word2[0])[0]
            list2 = get_list(word2,index)
            for a in list1:
                if a not in list2:
                    document.append(a)
        else:
            word2 = preprocess(word2[0])[0]
            list2 = get_list(word2,index)
            for a in list1:
                if a in list2:
                    document.append(a)
    elif "OR" in word2:        #if "OR" in word2
        word2.remove("OR")
        word2 = preprocess(word2[0])[0]
        list2 = get_list(word2,index)
        for a in list1:
            document.append(a)
        for b in list2 :
            if b not in document:
                document.append(b)
        document=map(int,document)  #change string to int for each element.
        document=sorted(document)
        document=[str(i) for i in document] #make sure document_id is string.
    else:  #   In this situation, word2 is empty.
        document=list1
    return document
"""
This function is to get retrieval rank.
Parameter "name" is the question ducument(txt). "index" means inverted index(dict) that I build before.
    "Output" is the file which I write results into.
"""
def tf_idf(name,index,result):
    f=open(name,"r")
    lines=f.readlines()
    queries=[]
    for line in lines:
        line=re.sub(r"^[0-9]+\s*","",line)
        line=preprocess(line)
        queries.append(line)
    weight={}
    number = len(xml_read("trec.5000.xml", "DOCNO"))
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
        rank=sorted(score.items(),key=lambda item:item[1],reverse=True)[:1000]
        print(rank)
        print_ranked(i+1,rank,result)
"""
The next part of the code is to call the function
"""
#inverted_index=get_index("trec.5000.xml")
#dict_write("dict.json",inverted_index)  #Training the model and write inverted index into a file
inverted_index = dict_read("dict.json")
#print_index(inverted_index,"index.txt")
research("queries.boolean.txt", inverted_index,"result.boolean.txt")
tf_idf("queries.ranked.txt",inverted_index,"result.ranked.txt")
'''
If the system cannot find document, please replace "*" to "TTDS/*" or use absolute path
'''
