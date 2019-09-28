# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:48:09 2019

@author: matth
"""
import re
import pickle
import spacy
import sys
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.linear_model import LogisticRegression

df_np = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np.p','rb'))

nlp = spacy.load(r'C:\Users\matth\Anaconda3\Lib\site-packages\en_core_web_sm\en_core_web_sm-2.1.0')

"""
CREATE FUNCTION TO CONVERT ABSTRACTS TO LISTS OF WORDS
"""
def removeSections(abstract): # remove words like conclusions, methods, etc
    abstract = abstract.lower()
    for replacers in ['conclusions:','conclusion:','result:','results:',
                  'background:','introduction:','methods:','objective:',
                  'objectives:','purpose:']:
        abstract = abstract.replace(replacers,'').strip()
    return abstract

def wordLister(abstract): #convert abstracts to lists
    abstract = removeSections(abstract)
    abstract = re.sub(r"([a-zA-Z])(\.)",r"\1REPLACEME555.",abstract)
    ablist = re.split('REPLACEME555\.',abstract)
    for sentence_index in range(len(ablist)):
        ablist[sentence_index] = ablist[sentence_index].strip()
    ablist.remove('')
    return ablist

"""
PROOF OF CONCEPT LOGISTIC REGRESSION
"""
"1) Create list of abstracts"
bow = [removeSections(abstract) for abstract in df_np.cleanabs]

"2) Create instance of countvectorizer class and fit abstract data"
counts = CountVectorizer(max_features=100,stop_words=STOP_WORDS)
counts = counts.fit_transform(bow)

"3) Create logistic regression data"
logreg = LogisticRegression()
logreg = logreg.fit(counts,df_np.approved)

"4) Simple descriptive statistics on the regression outputs"
coefs = logreg.coef_.tolist()[0]
feat = CountVectorizer(max_features=100,stop_words=STOP_WORDS).fit(bow).get_feature_names()
coefdict = {f:c for f,c in zip(feat,coefs)}
coefdict = {f:c for f,c in sorted(coefdict.items(), key=lambda item:item[1],reverse=True)}

coefdict