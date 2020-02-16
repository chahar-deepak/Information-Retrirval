File object is first parsed through BeautifulSoup's html parser to remove tags.
Now it is passed through nltk's word_tokenize function. It returns list of tokens
Tokens are then filtered to remove non-alphabets and non_numeric tokens (stored in 'string-tokens').

Stemming is done via PorterStemmer()
Lemmatization is done using WordNetLemmatizer

'plotting' function uses matplotlib library to plot most frequent 'plotting_element_count'-tokens

'getloglog' funtion takes dict of string:frequency and plots a log-log plot for Zipf's law analysis

'func' is a multipurpose funtion which internally calls above mentioned functions after calculating relevant parameters. It also calculates number of unique token to cover required X% of total tokens

'get_dict_of_bigrams' as implied, returns a dictionary of bigrams 'tuple of tokens':frequency

Chi-square is calculated and top 20 are printed

'anal_of_tokens' function is used to analyse stemming and lemmatization mistakes by manually inspecting after printing.
