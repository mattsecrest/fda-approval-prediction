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
import seaborn as sns
import sys
import altair as alt
import pickle
from sklearn.metrics import roc_curve, auc

sys.path.append('C:\\Users\\matth\\OneDrive\\Documents\\GitHub\\trials-and-fda')

"""
CREATE DATASET
"""
df = pickle.load(open(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\df_np_on.p','rb'))
cumusum = [i+1 for i in range(len(df.pubdate))]
df = df.sort_values(by='pubdate',ascending=True)
df['cumusum']=cumusum

" Initialize JSON"
url = '\static\cumsum.json'
df.to_json(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda'+url,orient='records')

"""
CREATE FIGURE 1 - CUMULATIVE SUM BY YEAR
"""
cs_chart = alt.Chart(url).mark_point(filled= True).encode(
    x = alt.X('pubdate:T',axis=alt.Axis(title="Publication Year")),
    y = alt.Y('cumusum:Q', axis=alt.Axis(title='Cumulative Count of Publications'))
    #color='approved:N',
    #opacity='approved:N'
)
cs_chart.save(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\static\cs_chart.json')

"""
CREATE KPTI DATASET
"""
kpti = pd.read_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\KPTI_20190101_20191008.csv',header=None)
kpti[1] = pd.to_datetime(kpti[1],format='%d-%b-%y')
kpti = kpti[(kpti[1]<pd.to_datetime('2019-09-01',format='%Y-%m-%d')) & (kpti[1]>pd.to_datetime('2019-04-01',format='%Y-%m-%d'))]

" Initialize JSON"
url2 = '\static\kpti.json'
kpti.to_json(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda'+url2,orient='records')
kpti = kpti.rename(columns={1:'date',2:'closing_price'})

"""
CREATE FIGURE 2 - KPTI CHARTS BY YEAR
"""
kpti_chart = alt.Chart(url2).mark_line().encode(
    x = alt.X('date:T',axis=alt.Axis(title="Date")),
    y = alt.Y('closing_price:Q', axis=alt.Axis(format='$',title='Closing Price'))
    #color='approved:N',
    #opacity='approved:N'
)
kpti_chart.save(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\static\kpti_chart.json')

"""
CREATE FIGURE 3 - ROC CURVE
"""
roc_data = np.array([['0.0', '0.058823529411764705', '0.058823529411764705',
        '0.058823529411764705', '0.0', '0.0', '0.47058823529411764',
        '0.5294117647058824', '0.4117647058823529', '0.0'],
       ['0.0', '0.0', '0.0', '0.0', '0.0', '0.00034494653328734045',
        '0.07726802345636426', '0.0776129699896516',
        '0.06036564332528458', '0.0'],
       ['Random Forest', 'Random Forest', 'Random Forest',
        'Random Forest', 'Random Forest', 'Random Forest', 'Naive Bayes',
        'Naive Bayes', 'Naive Bayes', 'Logistic Regression']],
      dtype='<U32')
roc = pd.DataFrame(data={'tp':roc_data[0],'fp':roc_data[1],'rg':roc_data[2]})

url3 = r'\static\roc.json'
roc.to_json(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda'+url3,orient='records')
roc_chart = alt.Chart(url3).mark_point(filled=True).encode(
        x = alt.X('fp:Q', scale=alt.Scale(domain=(0, 1)),axis=alt.Axis(title="False Positive Rate")),
        y = alt.Y('tp:Q', scale=alt.Scale(domain=(0, 1)),axis=alt.Axis(title='True Positive Rate')),
        color=alt.Color('rg:N',legend=alt.Legend(title="Regressor"))
    )
x,y = [0,1],[0,1]
xyd = pd.DataFrame(data={'x':x,'y':y})
xyc = alt.Chart(xyd).mark_line().encode(
        x='x:Q',
        y='y:Q'
    )

chartlayer = alt.layer(
      roc_chart,
      xyc
    ).configure_mark(
        color='green'
    )
chartlayer.save(r'C:\Users\matth\OneDrive\Documents\GitHub\trials-and-fda\static\roc_chart.json')
