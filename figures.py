# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:58:24 2019

@author: matth
"""
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pickle
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
import re
import matplotlib.pyplot as plt
import sys

sys.path.append('C:\\Users\\matth\\OneDrive\\Documents\\GitHub\\trials-and-fda')

from wordbag import removeSections

"""
FIGURE 1 - MOVING AVERAGE PUBLICATION COUNT
"""
df_np = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np.p','rb'))
moveave = []
for date in df_np.pubdate:
    datelow = date-pd.DateOffset(months=12)
    datehigh = date + pd.DateOffset(months=12)
    moveave.append(len(df_np.pubdate[(df_np.pubdate < datehigh)&(df_np.pubdate>datelow)]))

df_np['moveave']=moveave

plt.scatter(df_np.pubdate,df_np.moveave,s=10)
plt.xlabel('Year')
plt.ylabel('Moving Average Count per Year (N='+str(len(df_np.pubdate))+")")
plt.xlim(pd.to_datetime('1990-01-01',format='%Y-%m-%d'),
         pd.to_datetime('2018-12-31',format="%Y-%m-%d"))
plt.savefig(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\moveave.png',dpi=2000)

lines = []
for x in df_np[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)][['pubdate','SubStatusDateTime','moveave']].iterrows():
    temp = [[x[1][0],x[1][1]],[x[1][2],x[1][2]]]
    lines.append(temp)
    
plt.scatter(df_np.pubdate[df_np.approved==0],df_np.moveave[df_np.approved==0],s=15,c='aliceblue',zorder=1)
plt.scatter(df_np.pubdate[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)],df_np.moveave[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)],s=10,c='#1f77b4',zorder=2)
plt.scatter(df_np.SubStatusDateTime[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)],df_np.moveave[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)],s=10,c='green')
plt.plot_date(lines[0][0],lines[0][1],fmt='-',color='green',zorder=1)
for i in range(1,len(df_np[(df_np.approved==1) & (df_np.pubdate < df_np.SubStatusDateTime)])-1):
    plt.plot_date(lines[i][0],lines[i][1],fmt='-',color='green',zorder=1)   
plt.xlabel('Year')
plt.ylabel('Moving Average Count per Year (N='+str(len(df_np.pubdate))+")")
plt.xlim(pd.to_datetime('1990-01-01',format='%Y-%m-%d'),
         pd.to_datetime('2019-09-20',format="%Y-%m-%d"))
plt.savefig(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\moveaveapp2.png',dpi=2000)

"""
FIGURE 2 - WORD CLOUDS
"""
approvedab = ''
for abstract in df_np[df_np.approved==1].cleanabs:
    approvedab = approvedab+' '+removeSections(abstract)
    
notapproved = ''
for abstract in df_np[df_np.approved==0].cleanabs:
    notapproved = notapproved+' '+removeSections(abstract)
    
allabs = ''
for abstract in df_np.cleanabs:
    allabs = allabs+' '+removeSections(abstract)
    

appcloud = WordCloud(background_color='white').generate(approvedab)
notappcloud =  WordCloud().generate(notapproved)
allabscloud = WordCloud(background_color='white').generate(allabs)

plt.imshow(appcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

plt.imshow(notappcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

plt.imshow(allabscloud, interpolation='bilinear')
plt.axis("off")
plt.savefig(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\wordcloud.png',dpi=4000)


"""
FIGURE 3 
"""
