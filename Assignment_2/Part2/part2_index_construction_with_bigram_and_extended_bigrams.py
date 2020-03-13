#!/usr/bin/env python
# coding: utf-8

# In[9]:


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


#reading file
with open('../wiki_47',encoding='utf8') as file:
    content = file.read()


# In[3]:


soup = bs(content,'html.parser')
docs = soup.find_all('doc')


# In[4]:


#dic word->doc->doc->doc
#dic2 docid->word->word->word
dic = {}              # dictionary to store the term - documents and their frequency
dic_bigrams = {}      # dictionary to store the biwords - documents and their frequency
id_title = {}         #dictionary to store document id and their titles
dic2 = {}             #dictionary to store document id and all its terms with their corresponding normalized score
dic2_bigrams = {}     #dictionary to store document id and all its biwords with their corresponding normalized score


# In[5]:


set_of_stopwords = set(stopwords.words('english'))


# word->doc->doc->doc
# docid->word->word->word
before_processing = datetime.now()
doc_index = 0
for doc in docs:
    id = int(doc.get('id'))
    title = doc.get('title')
    
    id_title[id] = title
    
    data = doc.get_text()
    
    doc_index+=1
    
    
    #lemmatize the termsin the documents
    
    words = [ word.lower() for word in nltk.word_tokenize(data) if (word not in string.punctuation) ]
    
    words = [ WordNetLemmatizer().lemmatize(word,pos='v') for word in words]
    
    
    
    bigrams = []
    for i in range(len(words)-1):
        bigrams.append((words[i],words[i+1]))
        
        tmp = i+1
        while(tmp<len(words) and words[tmp] in set_of_stopwords):
            tmp += 1
        if(tmp != len(words) and tmp!=i+1):
            bigrams.append((words[i],words[tmp]))
    
    
    temp_dic = {}
    for word in set(words):
        temp_dic[word] = 0
    for word in words:
        if word in dic:
            dic[word] = dic[word] + [id]
        else:
            dic[word] = [id]
        
        
        temp_dic[word] += 1
    
    temp_dic_bigrams = {}
    for word in set(bigrams):
        temp_dic_bigrams[word] = 0
    for word in bigrams:
        if word in dic_bigrams:
            dic_bigrams[word] = dic_bigrams[word] + [id]
        else:
            dic_bigrams[word] = [id]
        
        
        temp_dic_bigrams[word] += 1

        ###########################################################################
        
    dic2[id] = temp_dic
    dic2_bigrams[id] = temp_dic_bigrams


# In[6]:


after_processing = datetime.now()

for every_doc in dic2:
    for every_word in dic2[every_doc]:
        dic2[every_doc][every_word]= (1 + log(dic2[every_doc][every_word],10))

        
for every_doc in dic2_bigrams:
    for every_word in dic2_bigrams[every_doc]:
        dic2_bigrams[every_doc][every_word]= (1 + log(dic2_bigrams[every_doc][every_word],10))        

# print('********************************************************************************************\n\n\n\n\n')
        
for every_doc in dic2:
    cumulate = 0
    for every_word in dic2[every_doc]:
        cumulate += dic2[every_doc][every_word]*dic2[every_doc][every_word]
    cumulate = sqrt(cumulate)

    #done individually for every doc
    for every_word in dic2[every_doc]:
        dic2[every_doc][every_word] /= cumulate
    #cosine normalized

for every_doc in dic2_bigrams:
    cumulate = 0
    for every_word in dic2_bigrams[every_doc]:
        cumulate += dic2_bigrams[every_doc][every_word]*dic2_bigrams[every_doc][every_word]
    cumulate = sqrt(cumulate)

    #done individually for every doc
    for every_word in dic2_bigrams[every_doc]:
        dic2_bigrams[every_doc][every_word] /= cumulate
#         cosine normalized
# print('********************************************************************************************\n\n\n\n\n\n')


# In[7]:


#dic representation change
for key in dic:
    temp_dic = {}
    ls = set(dic[key])
    for item in ls:
        temp_dic[item] = 0 
    for item in dic[key]:
        temp_dic[item]+=1
    
    dic[key] = temp_dic
    

for key in dic_bigrams:
    temp_dic = {}
    ls = set(dic_bigrams[key])
    for item in ls:
        temp_dic[item] = 0 
    for item in dic_bigrams[key]:
        temp_dic[item]+=1
    
    dic_bigrams[key] = temp_dic


# In[10]:


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

outfile = open('dic_bigrams','wb')
pickle.dump(dic_bigrams,outfile)
outfile.close()

outfile = open('dic2_bigrams','wb')
pickle.dump(dic2_bigrams,outfile)
outfile.close()


# In[ ]:


# def document_freq(word):
#     try:
#         return len(dic[word])
#     except:
#         return len(docs)


# def calculate(word):
#     tf = dict_of_IP[word]
#     df = document_freq(word)
    
#     score = (1+log(tf,10))*(log(len(docs)/df))
#     return score


# def document_freq_bigrams(word):
#     try:
#         return len(dic_bigrams[word])
#     except:
#         return len(docs)


# def calculate_bigrams(word):
#     tf = dict_of_IP_bigrams[word]
#     df = document_freq_bigrams(word)
    
#     score = (1+log(tf,10))*(log(len(docs)/df))
#     return score


# In[ ]:


# def calculate_final_score(id):
#     value =0 
#     for query_term in dict_of_raw_score:
#         try:
#             value +=dict_of_raw_score[query_term]*dic2[id][query_term]
#         except:
#             value += 0
    
#     return value


# def calculate_final_score_bigrams(id):
#     value =0 
#     for query_term in dict_of_raw_score_bigrams:
#         try:
#             value +=dict_of_raw_score_bigrams[query_term]*dic2_bigrams[id][query_term]
#         except:
#             value += 0
    
#     return value


# In[ ]:


# while(1):
#     input_tokens = [token.lower() for token in word_tokenize(input("Search for:")) if ( token not in string.punctuation)]
#     if(len(input_tokens)==0):
#         print("...")
#         break
    
#     input_tokens = [ WordNetLemmatizer().lemmatize(word,pos='v') for word in input_tokens]
    
#     input_tokens_bigrams = []
#     for i in range(len(input_tokens)-1):
#         input_tokens_bigrams.append((input_tokens[i],input_tokens[i+1]))
#         tmp = i+1
#         while(tmp<len(input_tokens) and input_tokens[tmp] in set_of_stopwords):
#             tmp += 1
#         if(tmp != len(input_tokens) and tmp!=i+1):
#             input_tokens_bigrams.append((input_tokens[i],input_tokens[tmp]))
            
    

#     ##############################3        
            
            
#     dict_of_IP = {}
#     dict_of_IP_bigrams = {}

#     set_of_input_tokens = set(input_tokens)
#     set_of_input_tokens_bigrams = set(input_tokens_bigrams)

#     for word in set_of_input_tokens:
#         dict_of_IP[word] = 0
#     for word in set_of_input_tokens_bigrams:
#         dict_of_IP_bigrams[word] = 0

#     for word in input_tokens:
#         dict_of_IP[word] += 1
#     for word in input_tokens_bigrams:
#         dict_of_IP_bigrams[word] += 1

    
#     ###############################################################
    
#     dict_of_raw_score = {}
#     for word in set_of_input_tokens:
#         dict_of_raw_score[word] = calculate(word)

#     denominator = 0
#     for word in dict_of_raw_score:
#         temp = dict_of_raw_score[word]
#         denominator += temp*temp

#     denominator = sqrt(denominator)

#     for word in dict_of_raw_score:
#         try:
#             dict_of_raw_score[word] /= denominator
#         except:
#             dict_of_raw_score[word] = 0
            
            
            
#     dict_of_raw_score_bigrams = {}
#     for word in set_of_input_tokens_bigrams:
#         dict_of_raw_score_bigrams[word] = calculate_bigrams(word)

#     denominator = 0
#     for word in dict_of_raw_score_bigrams:
#         temp = dict_of_raw_score_bigrams[word]
#         denominator += temp*temp

#     denominator = sqrt(denominator)

#     for word in dict_of_raw_score_bigrams:
#         try:
#             dict_of_raw_score_bigrams[word] /= denominator
#         except:
#             dict_of_raw_score_bigrams[word] = 0
    
    
    
    
#     set_of_relevant_docs = set()
#     for input_term in set_of_input_tokens:
#         try:
#             temp_dic = dic[input_term]
#         except:
#             temp_dic = {}

#         for relevant_ids in temp_dic:
#             set_of_relevant_docs.add(relevant_ids)


#     set_of_relevant_docs_bigrams = set()
#     for input_term in set_of_input_tokens_bigrams:
#         try:
#             temp_dic = dic_bigrams[input_term]
#         except:
#             temp_dic = {}

#         for relevant_ids in temp_dic:
#             set_of_relevant_docs_bigrams.add(relevant_ids)
    
    
#     final_score = {}
#     final_score_bigrams = {}
    
    
#     for doc in docs:
#         id = int(doc.get('id'))

#         if(id not in set_of_relevant_docs):
#             final_score[id] = 0
#         else:
#             final_score[id] = calculate_final_score(id)

#         if(id not in set_of_relevant_docs_bigrams):
#             final_score_bigrams[id] = 0
#         else:
#             final_score_bigrams[id] = calculate_final_score_bigrams(id)

    
#     sor = sorted(final_score.items(),key = operator.itemgetter(1),reverse=True)
#     sor_bigrams = sorted(final_score_bigrams.items(),key = operator.itemgetter(1),reverse=True)
    
    
#     unique_result_set = set()
#     count = 10
#     if(len(sor_bigrams)>0 and sor_bigrams[0][1] > 0):
#         print("Result using bigrams:\n")
    
#     for i in sor_bigrams:
#         x = i[0]
#         y = i[1]
#         if( count>0 and y!=0):
#             print(x,' score: ',y ,'\t' ,id_title[x])
#             unique_result_set.add(x)
#         else:
#             break
#             print(docs[x].get_text())
#         count -=1
    
#     print("\n")
#     if(count != 0):
#         print("Result using unigrams:\n")
#         for i in sor:
            
#             x = i[0]
#             y = i[1]
#             if(x not in unique_result_set):
#                 if( count>0):
#                     print(x,' score: ',y ,'\t' ,id_title[x])
#                 else:
#                     break
#                 count -= 1 
    


# In[ ]:




