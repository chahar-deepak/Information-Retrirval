#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
from bs4 import BeautifulSoup as bs
import nltk
from nltk.tokenize import word_tokenize
import string
import operator
from math import log,sqrt
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


# In[3]:


#reading file
with open('../wiki_47',encoding='utf8') as file:
    content = file.read()
    
#html parsing
soup = bs(content,'html.parser')
docs = soup.find_all('doc')


# In[4]:


#calculate the final score that the document gets for the given query

def calculate_final_score(id):
    value =0 
    for query_term in dict_of_raw_score:
        try:
            value +=dict_of_raw_score[query_term]*dic2[id][query_term]
        except:
            value += 0
    
    return value


# In[5]:


#returns the document freq of the term passed
def document_freq(word):
    try:
        return len(dic[word])
    except:
        return len(docs)


#calculate the tf-idf score of the query term
def calculate(word):
    tf = dict_of_IP[word]
    df = document_freq(word)
    
    
    score = (1+log(tf,10))*(log(len(docs)/df))
    return score


# In[7]:


while(1):
    input_tokens = [token.lower() for token in word_tokenize(input("Search for:")) if ( token not in string.punctuation)]
    
    if(len(input_tokens) == 0 ):
        print("Exiting...")
        break
    
    
    dict_of_IP = {}
    set_of_input_tokens = set(input_tokens)
    for word in set_of_input_tokens:
        dict_of_IP[word] = 0

    for word in input_tokens:
        dict_of_IP[word] += 1

    
    ###################################
    
    dict_of_raw_score = {}
    for word in set_of_input_tokens:
        dict_of_raw_score[word] = calculate(word)

    denominator = 0
    for word in dict_of_raw_score:
        temp = dict_of_raw_score[word]
        denominator += temp*temp

    denominator = sqrt(denominator)
    
    #########################################
    
    for word in dict_of_raw_score:
        try:
            dict_of_raw_score[word] /= denominator
        except:
            dict_of_raw_score[word] = 0
        
        
    ############################################
    
    set_of_relevant_docs = set()
    for input_term in set_of_input_tokens:
        try:
            temp_dic = dic[input_term]
        except:
            temp_dic = {}

        for relevant_ids in temp_dic:
            set_of_relevant_docs.add(relevant_ids)

    ##############################################
    
    final_score = {}
    for doc in docs:
        id = int(doc.get('id'))

        if(id not in set_of_relevant_docs):
            final_score[id] = 0
        else:
            final_score[id] = calculate_final_score(id)

    ###############################################
    
    sor = sorted(final_score.items(),key = operator.itemgetter(1),reverse=True)
    
    count = 0
    for i in sor:
        count +=1
        x = i[0]
        y = i[1]
        if(y and count<=10):
            print(x,' score: ',y ,'\t' ,id_title[x])
        else:
            break
    
    


# In[ ]:




