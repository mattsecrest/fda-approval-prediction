from flask import Flask, render_template, request, redirect,flash,url_for,session
from wtforms import Form, FloatField, validators
from forms import Abstract, goBack
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import BoxSelectTool, BoxZoomTool,ResetTool,WheelZoomTool,LassoSelectTool
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e256803842b0ac38c491bc4ff193e809587b1ef2b6915b9cd746b46b8978883a'

@app.route('/', methods = ['GET','POST'])
def index():
    form = Abstract()
    if request.method=="POST":
        if form.validate_on_submit():
            session['abstract']=form.abstract.data
            return redirect(url_for('prediction'))
        else:
            flash("Try again.")
            return render_template("index.html",form=form)
    return render_template("index.html",form=form)

@app.route('/prediction',methods = ['GET','POST'])
def prediction():
    back = goBack()
    if back.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('prediction.html', script=script, div=div,form=back)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)