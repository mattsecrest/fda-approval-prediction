from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class Abstract(FlaskForm):
    symbol = StringField('Abstract',
                           validators=[DataRequired()])
                           
    submit = SubmitField('Confirm')

class goBack(FlaskForm):
    back = SubmitField("Back")