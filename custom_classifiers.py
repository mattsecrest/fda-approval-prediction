# -*- coding: utf-8 -*-
"""
Created on Thu Oct  10 16:24:18 2019

@author: matth
"""

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
from sklearn.ensemble import RandomForestClassifier
import numpy as np


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
    
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
