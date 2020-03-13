#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importng relevant libraries
from datetime import datetime
from bs4 import BeautifulSoup as bs
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import bigrams
import string
import operator
from nltk.corpus import stopwords
from math import log,sqrt
import sys
import pickle


# In[2]:


# importing all the pickles file which stores the inverted index constructed

infile = open('dic_out','rb')
dic = pickle.load(infile)
infile.close()

infile = open('dic2_out','rb')
dic2 = pickle.load(infile)
infile.close()

infile = open('id_title','rb')
id_title = pickle.load(infile)
infile.close()

infile = open('dic_bigrams','rb')
dic_bigrams = pickle.load(infile)
infile.close()

infile = open('dic2_bigrams','rb')
dic2_bigrams = pickle.load(infile)
infile.close()


# In[3]:


#reading file
with open('../wiki_47',encoding='utf8') as file:
    content = file.read()
    
#html parsing
soup = bs(content,'html.parser')
docs = soup.find_all('doc')

set_of_stopwords = set(stopwords.words('english'))


# In[4]:


def document_freq(word):
    try:
        return len(dic[word])
    except:
        return len(docs)


def calculate(word):
    tf = dict_of_IP[word]
    df = document_freq(word)
    
    score = (1+log(tf,10))*(log(len(docs)/df))
    return score


def document_freq_bigrams(word):
    try:
        return len(dic_bigrams[word])
    except:
        return len(docs)


def calculate_bigrams(word):
    tf = dict_of_IP_bigrams[word]
    df = document_freq_bigrams(word)
    
    score = (1+log(tf,10))*(log(len(docs)/df))
    return score


# In[5]:


def calculate_final_score(id):
    value =0 
    for query_term in dict_of_raw_score:
        try:
            value +=dict_of_raw_score[query_term]*dic2[id][query_term]
        except:
            value += 0
    
    return value


def calculate_final_score_bigrams(id):
    value =0 
    for query_term in dict_of_raw_score_bigrams:
        try:
            value +=dict_of_raw_score_bigrams[query_term]*dic2_bigrams[id][query_term]
        except:
            value += 0
    
    return value


# In[7]:


while(1):
    input_tokens = [token.lower() for token in word_tokenize(input("Search for:")) if ( token not in string.punctuation)]
    if(len(input_tokens)==0):
        print("Exiting...")
        break
    
    input_tokens = [ WordNetLemmatizer().lemmatize(word,pos='v') for word in input_tokens]
    
    input_tokens_bigrams = []
    for i in range(len(input_tokens)-1):
        input_tokens_bigrams.append((input_tokens[i],input_tokens[i+1]))
        tmp = i+1
        while(tmp<len(input_tokens) and input_tokens[tmp] in set_of_stopwords):
            tmp += 1
        if(tmp != len(input_tokens) and tmp!=i+1):
            input_tokens_bigrams.append((input_tokens[i],input_tokens[tmp]))
            
    

    ##############################3        
            
            
    dict_of_IP = {}
    dict_of_IP_bigrams = {}

    set_of_input_tokens = set(input_tokens)
    set_of_input_tokens_bigrams = set(input_tokens_bigrams)

    for word in set_of_input_tokens:
        dict_of_IP[word] = 0
    for word in set_of_input_tokens_bigrams:
        dict_of_IP_bigrams[word] = 0

    for word in input_tokens:
        dict_of_IP[word] += 1
    for word in input_tokens_bigrams:
        dict_of_IP_bigrams[word] += 1

    
    ###############################################################
    
    dict_of_raw_score = {}
    for word in set_of_input_tokens:
        dict_of_raw_score[word] = calculate(word)

    denominator = 0
    for word in dict_of_raw_score:
        temp = dict_of_raw_score[word]
        denominator += temp*temp

    denominator = sqrt(denominator)

    for word in dict_of_raw_score:
        try:
            dict_of_raw_score[word] /= denominator
        except:
            dict_of_raw_score[word] = 0
            
            
            
    dict_of_raw_score_bigrams = {}
    for word in set_of_input_tokens_bigrams:
        dict_of_raw_score_bigrams[word] = calculate_bigrams(word)

    denominator = 0
    for word in dict_of_raw_score_bigrams:
        temp = dict_of_raw_score_bigrams[word]
        denominator += temp*temp

    denominator = sqrt(denominator)

    for word in dict_of_raw_score_bigrams:
        try:
            dict_of_raw_score_bigrams[word] /= denominator
        except:
            dict_of_raw_score_bigrams[word] = 0
    
    
    
    
    set_of_relevant_docs = set()
    for input_term in set_of_input_tokens:
        try:
            temp_dic = dic[input_term]
        except:
            temp_dic = {}

        for relevant_ids in temp_dic:
            set_of_relevant_docs.add(relevant_ids)


    set_of_relevant_docs_bigrams = set()
    for input_term in set_of_input_tokens_bigrams:
        try:
            temp_dic = dic_bigrams[input_term]
        except:
            temp_dic = {}

        for relevant_ids in temp_dic:
            set_of_relevant_docs_bigrams.add(relevant_ids)
    
    
    final_score = {}
    final_score_bigrams = {}
    
    
    for doc in docs:
        id = int(doc.get('id'))

        if(id not in set_of_relevant_docs):
            final_score[id] = 0
        else:
            final_score[id] = calculate_final_score(id)

        if(id not in set_of_relevant_docs_bigrams):
            final_score_bigrams[id] = 0
        else:
            final_score_bigrams[id] = calculate_final_score_bigrams(id)

    
    sor = sorted(final_score.items(),key = operator.itemgetter(1),reverse=True)
    sor_bigrams = sorted(final_score_bigrams.items(),key = operator.itemgetter(1),reverse=True)
    
    
    unique_result_set = set()
    count = 10
    if(len(sor_bigrams)>0 and sor_bigrams[0][1] > 0):
        print("Result using bigrams:\n")
    
    for i in sor_bigrams:
        x = i[0]
        y = i[1]
        if( count>0 and y!=0):
            print(x,' score: ',y ,'\t' ,id_title[x])
            unique_result_set.add(x)
        else:
            break
            print(docs[x].get_text())
        count -=1
    
    print("\n")
    if(count != 0):
        print("Result using unigrams:\n")
        for i in sor:
            
            x = i[0]
            y = i[1]
            if(x not in unique_result_set):
                if( count>0):
                    print(x,' score: ',y ,'\t' ,id_title[x])
                else:
                    break
                count -= 1 
    


# In[ ]:




