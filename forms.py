from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired

class Abstract(FlaskForm):
    abstract = TextAreaField('Abstract',
                           validators=[InputRequired()])
                           
    submit = SubmitField('Confirm')

class goBack(FlaskForm):
    back = SubmitField("Back")