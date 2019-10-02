from flask import Flask, render_template, request, redirect,flash,url_for,session
from wtforms import Form, FloatField, validators
from forms import Abstract, goBack
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import BoxSelectTool, BoxZoomTool,ResetTool,WheelZoomTool,LassoSelectTool
import pandas as pd
from config import Config

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
    if back.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('prediction.html')

@app.route('/about',methods=['GET','POST'])
def about():
   return render_template("about.html")
 
@app.route('/how',methods=['GET','POST'])
def how():
   return render_template("how.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)