from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer
import numpy
import matplotlib.pyplot as plt
from nltk import FreqDist
import operator
import nltk
from math import log
# nltk.download('wordnet')


# Constants
scaling_factor=1.4
plotting_element_count = 40


with open('wiki_69','rt',encoding='utf8') as file:
    content = file.read()

raw_data = BeautifulSoup(content,'html.parser').get_text()
tokens = word_tokenize(raw_data)
# type(tokens) is list


string_tokens = [ token.lower() for token in tokens if token.isalpha() ]
# print(len(string_tokens))


stemmed_words = []
lemmatized_words = []
for word in string_tokens:
    stemmed_words.append(PorterStemmer().stem(word))
    lemmatized_words.append(WordNetLemmatizer().lemmatize(word))


# Functions
def plotting(didi,string):
    x=[]
    y=[]
    for i in list(didi)[:plotting_element_count]:
        x.append(i)
        y.append(didi[i])

    plt.figure(figsize=(scaling_factor*16,scaling_factor*9))
    plt.title(string)
    plt.xlabel(string)
    plt.ylabel('Frequency of occurence')
    plt.xticks(rotation=90)
    plt.bar(x,y,width=0.9/scaling_factor)
    plt.savefig(string+'.png')
    

def getloglog(didi,string):
    num = len(didi)
#     Ranking starts from 1
    x = [x for x in range(1,num+1)]
    
    y =[]
    for i in didi.values():
        y.append(i)
    
    plt.figure(figsize=(scaling_factor*9,scaling_factor*9))
    plt.title('Log-Log plot for '+string)
    plt.xlabel('Ranking according to Frequency')
    plt.loglog(x,y)
    plt.savefig('Log-Log plot for '+string+'.png')


def func(list_of_tokens,string):    
    # Getting number of unique unigrams
    unique_unigrams = set(list_of_tokens)
    print("Unique "+string+"unigrams: ", len(unique_unigrams))  


    didi = { x:0 for x in unique_unigrams}
    for x in list_of_tokens:
        didi[x]+=1

    didi = dict(sorted(didi.items(), key=operator.itemgetter(1),reverse=True))
    dict_of_unigrams=didi.copy()
    
    # Calling relevant functions
    getloglog(didi,string + 'Unigrams')
    plotting(didi,string + 'Unigrams')
    

    # Number of unigrams required to cover 90%    
    target = int(0.9*len(list_of_tokens))
    # print('Target is ',target)

    net = 0
    count = 0
    for i in didi:
        if(net < target):
            net+= didi[i]
            count += 1
        else:
            print('Unique '+string+'unigrams to cover 90%: ',count, ' out of ',len(unique_unigrams))
            break
    
    ######################## Bigrams ############################
    
    list_of_bigrams = list(nltk.bigrams(list_of_tokens))
    returning_list_of_bigrams = list_of_bigrams.copy()
    list_of_bigrams = [ '('+x[0]+','+x[1]+')' for x in list_of_bigrams ] 
    
    unique_bigrams = set(list_of_bigrams)
    print("Unique "+string+"bigrams: ",len(unique_bigrams))
    
    
    didi = { x:0 for x in unique_bigrams}
    for x in list_of_bigrams:
        didi[x]+=1
    
    didi = dict(sorted(didi.items(), key=operator.itemgetter(1),reverse=True))
    
    
    # Calling relevant functions
    getloglog(didi,string + 'Bigrams') 
    plotting(didi,string + 'Bigrams')
    
    
    # Number of bigrams required to cover 80%
    target = int(0.8*len(list_of_bigrams))
    
    net = 0
    count = 0
    for i in didi:
        if(net < target):
            net+= didi[i]
            count += 1
        else:
            print('Unique '+string+'bigrams to cover 80%: ',count, ' out of ',len(unique_bigrams))
            break

    ######################## Trigrams ############################
    
    list_of_trigrams = list(nltk.trigrams(list_of_tokens))
    list_of_trigrams = [ '('+x[0]+','+x[1]+','+x[2]+')' for x in list_of_trigrams ] 
    
    unique_trigrams = set(list_of_trigrams)
    print("Unique "+string+"trigrams: ",len(unique_trigrams))
    

    didi = { x:0 for x in unique_trigrams}
    for x in list_of_trigrams:
        didi[x]+=1
    
    didi = dict(sorted(didi.items(), key=operator.itemgetter(1),reverse=True))

    # Calling relevant functions
    getloglog(didi,string + 'Trigrams')
    plotting(didi,string + 'Trigrams')
    
    
    # Number of trigrams required to cover 70%
    target = int(0.7*len(list_of_trigrams))
    
    net = 0
    count = 0
    for i in didi:
        if(net < target):
            net+= didi[i]
            count += 1
        else:
            print('Unique '+string+'trigrams to cover 70%: ',count, ' out of ',len(unique_trigrams))
            break
    
    return dict_of_unigrams,returning_list_of_bigrams


def get_dict_of_bigrams(list_of_bigrams):
    dict_of_bigrams = { x:0 for x in set(list_of_bigrams)}
    for x in list_of_bigrams:
        dict_of_bigrams[x]+=1
    return dict_of_bigrams


# Function calling
dict_of_unigrams,list_of_bigrams = func(string_tokens,'')
_,_ = func(stemmed_words,'Stemmed ')
_,_ =  func(lemmatized_words,'Lemmatized ')


dict_of_bigrams = get_dict_of_bigrams(list_of_bigrams)

# Calculations for chisquare bigram dictionary
chisq = dict_of_bigrams.copy()
total = len(string_tokens)
for key in dict_of_bigrams:
    o11 = dict_of_bigrams[key]
    o21 = dict_of_unigrams[key[0]] - o11
    o12 = dict_of_unigrams[key[1]] - o11
    o22 = total-o11-o12-o21
    
    chisq[key] = float((total*(o11*o22-o12*o21)^2))/((o11+o12)*(o11+o21)*(o12+o22)*(o21+o22))


list_of_chisq = list(sorted(chisq.items(),key=operator.itemgetter(1),reverse=True))


print("20 Collocation elements are:")
count=0
for i,value in list_of_chisq[:20]:
    count+=1
    print(count,i)


def anal_of_tokens(string_tokens,stemmed_words,lemmatized_words):
    dict_of_stemmed_words = {x:set() for x in set(stemmed_words)}
    dict_of_lemmatized_words = {x:set() for x in set(lemmatized_words)}
    
    for i in string_tokens:
        stemmed = PorterStemmer().stem(i)
        ltized = WordNetLemmatizer().lemmatize(i)
        dict_of_stemmed_words[stemmed].add(i)
        dict_of_lemmatized_words[ltized].add(i)
        
        for i in dict_of_stemmed_words.items():
            if(len(i[1])>2):
                print(i[0],'\t',i[1])
        
        for i in dict_of_lemmatized_words.items():
            if(len(i[1])>=2):
                print(i[0],'\t',i[1],'\n')

# function to analyse stemmed ad lemmatized words  by printing them with non-processed tokens
# anal_of_tokens(string_tokens,stemmed_words,lemmatized_words)