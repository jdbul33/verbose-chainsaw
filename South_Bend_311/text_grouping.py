# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 23:14:57 2018

@author: jdbul
"""

"""

Reducing the number of call topics using NLP

"""
#%%
"""
Set up and package import
"""


import nltk

"""
Download the following data from nltk to run script
nltk.download('punkt')
nltk.download('stopwords')
"""

print(len(topics.Topic.unique()))
print(len(topics.Topic))

tokenizer = nltk.word_tokenize

#%%
"""
Create tokenizing function
"""


def tokenize_it_all(s):
    """
    This function will iterate over a series and tokenize words.
    It returns a list of lists
    """
    toks = []
    for i in range(len(s)):
        words = tokenizer(s[i])
        toks.append(words)
    return toks

#%%

tokens = tokenize_it_all(topics.Topic)

stopwords = nltk.corpus.stopwords.words('english')

tokens_clean = []

for i in range(len(tokens)):
    x = []
    x.append([word for word in tokens[i] if word not in stopwords])
    tokens_clean.append(x)
    
#%%
"""
At this point, tokens have been created and cleaned for stop words
"""




