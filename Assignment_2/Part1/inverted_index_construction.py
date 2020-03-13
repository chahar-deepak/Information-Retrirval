#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importng relevant libraries
from datetime import datetime
from bs4 import BeautifulSoup as bs
import nltk
from nltk.tokenize import word_tokenize
import string
import operator
from math import log,sqrt
import pickle


# In[2]:


#opening and reading file
with open('../wiki_47',encoding='utf8') as file:
    content = file.read()


# In[3]:


#html parsing
soup = bs(content,'html.parser')
docs = soup.find_all('doc')


# In[4]:


#dic word->doc->doc->doc
#dic2 docid->word->word->word
dic = {}     # dictionary to store the term - documents and their frequency
id_title = {}    #dictionary to store document id and their titles
dic2 = {}       #dictionary to store document id and all its terms with their corresponding normalized score


# In[5]:


# word->doc->doc->doc
# docid->word->word->word

#populating the dictionaries

doc_index = 0
for doc in docs:
    id = int(doc.get('id'))
    title = doc.get('title')
    
    id_title[id] = title
    
    data = doc.get_text()
    
    doc_index+=1
    
    
    words = [ word.lower() for word in nltk.word_tokenize(data) if (word not in string.punctuation) ]
    
    temp_dic = {}
    for word in set(words):
        temp_dic[word] = 0
    
    
    
    
    for word in words:
        if word in dic:
            dic[word] = dic[word] + [id]
        else:
            dic[word] = [id]
        
        
        temp_dic[word] += 1

        ###########################################################################
        
    dic2[id] = temp_dic


# In[6]:


# term frequency lnc impleantation
# dic2[every_doc][every_word] tells term frequency

for every_doc in dic2:
    for every_word in dic2[every_doc]:
        dic2[every_doc][every_word]= (1 + log(dic2[every_doc][every_word],10))

        
for every_doc in dic2:
    cumulate = 0
    for every_word in dic2[every_doc]:
        cumulate += dic2[every_doc][every_word]*dic2[every_doc][every_word]
    cumulate = sqrt(cumulate)

    #done individually for every doc
    for every_word in dic2[every_doc]:
        dic2[every_doc][every_word] /= cumulate
    #cosine normalized


# In[7]:


for key in dic:
    temp_dic = {}
    ls = set(dic[key])
    for item in ls:
        temp_dic[item] = 0 
    for item in dic[key]:
        temp_dic[item]+=1
    
    dic[key] = temp_dic


# In[8]:


# storing all the dictionaries as pickle file which will be used in test_queries.py file

outfile = open('dic_out','wb')
pickle.dump(dic,outfile)
outfile.close()

outfile = open('dic2_out','wb')
pickle.dump(dic2,outfile)
outfile.close()

outfile = open('id_title','wb')
pickle.dump(id_title,outfile)
outfile.close()

