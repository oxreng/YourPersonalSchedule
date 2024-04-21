from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from datetime import date


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start = DateField('Start Date', validators=[DataRequired()], default=date.today)
    end = DateField('End Date', validators=[DataRequired()], default=date.today)
    color = StringField('Color', validators=[DataRequired()])