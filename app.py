from flask import Flask, render_template, request, redirect,flash,url_for,session
from wtforms import Form, FloatField, validators
from forms import Abstract, goBack
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import BoxSelectTool, BoxZoomTool,ResetTool,WheelZoomTool,LassoSelectTool
from custom_classifiers import cleanAbs,extractPequals,LemmaTokenizer
import pandas as pd
from config import Config
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

bestimator = pickle.load(open('bestimator.p','rb'))
fn = pickle.load(open('fn.p','rb'))
words_z = pickle.load(open('words_z.p','rb'))

app = Flask(__name__)

app.config.from_object(Config)  

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
    form = Abstract()
    if request.method=="POST":
        if form.validate_on_submit():
            session['abstract']=form.abstract.data
            return redirect(url_for('prediction'))
        else:
            flash("Try again.")
            return render_template("index.html",form=form)
    else:   
        return render_template("index.html",form=form)

@app.route('/prediction',methods = ['GET','POST'])
def prediction():
    back = goBack()
    outdict = {}
    outstr = ''
    for word in session['abstract'].split(' '):
        if word in words_z:
            outdict[word] = words_z[word]
            outstr += word + ",\n"
    if not outdict:
        outstr='No relevant features'
        script = ''
        div = ''
      
    elif outdict:
        outstr=outstr[:-2]
        outdict = {key:val for key, val in sorted(outdict.items(), key=lambda item: item[1], reverse = True)}
        x = list(outdict.keys())
        y = list(outdict.values())
        p = figure(x_range=x, plot_height=250, title="Words contributing to prediction", toolbar_location = None, tools="")
        p.vbar(x = x, top = y, width = 0.9)
        p.yaxis.axis_label = 'Relative contribution'
        p.xaxis.major_label_orientation = "vertical"
        script,div = components(p)
        
    est = round(bestimator.predict_proba([session['abstract']])[0][1]*100,2)
    
    if back.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('prediction.html',est = est,outstr=outstr, script = script, div = div)

@app.route('/about',methods=['GET','POST'])
def about():
   return render_template("about.html")
 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)