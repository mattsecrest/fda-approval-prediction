# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 14:18:18 2019

@author: matth
"""

"BRING IN IMPORTANT MODULES"
import pandas as pd
import pickle
from sklearn import model_selection
from sklearn import base, preprocessing, neighbors, model_selection
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
import spacy
from spacy.lemmatizer import Lemmatizer
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as esw
import re
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression
import numpy as np

"LOAD MAIN ANALYTIC DATASET"
df = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np_on.p','rb'))

"START EXTRACTING FEATURES"
"1) Separate into train and test sets and numpy arrays"
x_train, x_test, y_train, y_test = [i.to_numpy() for i in model_selection.train_test_split(df.crudeabs, df.approved, test_size=0.2, shuffle=True, random_state=42)]

"2) Clean abstracts"
def removeSections(abstract):
    abstract = abstract.lower()
    # First remove major section headers
    for firstreplacers in ['conclusions:','conclusion:','result:','results:',
                  'background:','introduction:','methods:','objective:',
                  'objectives:','purpose:','aims: ','clinicaltrials.gov',
                  'context', 'design and settings']:
        abstract = abstract.replace(firstreplacers,'').strip()
        
    # Then remove copyright symbols
    for cr in [u'\N{COPYRIGHT SIGN}','copyright']:
        abstract = re.sub(cr+'.*','',abstract)
        
    # Remove NCT numbers
    abstract = re.sub('nct\d{8}','',abstract)
    
    # Replace some odd values
    abstract = re.sub('\N{MIDDLE DOT}','.',abstract)
    
    return abstract

"3) Create extract p function"
def p_valEquals(abstract): # This will take the value of 0 (does not exist), 1 (at least one p-value lower than 0.05), 2 (p-values exist but none lower than 0.05)
    out = 0
    ps = [float(out[-1]) for out in re.findall('([P{0,1}|p{0,1}]\-{0,1}(value){0,1}\s{0,1}\=\s{0,1})([0,9]\.[0-9]{0,5})',abstract)]
    if ps != []:
        out = 2
        for pval in ps:
            if pval<=0.05:
                out = 1
    return out

"4) Create clean abstracts transformer"
class cleanAbs(base.BaseEstimator, base.RegressorMixin):
    def __init__(self):
        return None
    
    def fit(self,X,y):
        return self
    
    def transform(self,X,y=None):
        o = []
        for x in X:
            o.append(self.removeSections(x))
        return o
    
    def removeSections(self,abstract):
        abstract = abstract.lower()
        # First remove major section headers
        for firstreplacers in ['conclusions:','conclusion:','result:','results:',
                      'background:','introduction:','methods:','objective:',
                      'objectives:','purpose:','aims: ','clinicaltrials.gov',
                      'context', 'design and settings']:
            abstract = abstract.replace(firstreplacers,'').strip()
            
        # Then remove copyright symbols
        for cr in [u'\N{COPYRIGHT SIGN}','copyright']:
            abstract = re.sub(cr+'.*','',abstract)
            
        # Remove NCT numbers
        abstract = re.sub('nct\d{8}','',abstract)
        
        # Replace some odd values
        abstract = re.sub('\N{MIDDLE DOT}','.',abstract)
        
        return abstract

"5) Create extractP transformer"
class extractPequals(base.BaseEstimator, base.RegressorMixin):
    def __init__(self):
        return None
    
    def fit(self,X,y):
        return self
    
    def transform(self,X,y=None):
        o = []
        for x in X:
            o.append(self.p_valEquals(x))
        return o    
            
    def p_valEquals(self, abstract): # This will take the value of 0 (does not exist), 1 (at least one p-value lower than 0.05), 2 (p-values exist but none lower than 0.05)
        out = 0
        ps = [float(out[-1]) for out in re.findall('([P{0,1}|p{0,1}]\-{0,1}(value){0,1}\s{0,1}\=\s{0,1})([0,9]\.[0-9]{0,5})',abstract)]
        if ps != []:
            out = 2
            for pval in ps:
                if pval<=0.05:
                    out = 1
        return out
    

"6) Create Lemmatizer"
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

"7) Create the pipeline for the clean abstract count vectorizer"
cleanAbsPipe = Pipeline([
        ('cA',cleanAbs()),
        ('cV',TfidfVectorizer(tokenizer=LemmaTokenizer())),
        ('tsvd',TruncatedSVD()),
        ('lr',LogisticRegression())
        ])

cleanAbsParams = {
        'cV__max_df':[.95],
        'cV__min_df':[.05],
        'cV__stop_words':['english'],
        'cV__ngram_range':[(1,1)],
        'tsvd__n_components':[2]
        }
    
cleanAbsPipeCV = model_selection.GridSearchCV(cleanAbsPipe,cleanAbsParams,
                                              cv=4,verbose=10,return_train_score=True)

"""
CREATE PREDICTIVE MODEL
"""
"Fit the predictive model on the training set"
cleanAbsPipeCV.fit(x_train,y_train)

"Evaluate performance"
cleanAbsPipeCV.cv_results_

bestimator = cleanAbsPipeCV.best_estimator_

"Pickle best estimatar for the Heroku app"
#pickle.dump(bestimator,open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\bestimator.p','wb'))

"""
PLAY AROUND WITH ESTIMATOR OUTPUTS
"""
abstract = x_test[0]

bestimator.predict([abstract])
