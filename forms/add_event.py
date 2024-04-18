from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length
import datetime as dt


class AddEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()],
                           default=dt.datetime.now().date())
    end_date = DateField('End Date', validators=[DataRequired()],
                         default=dt.datetime.now().date())
    submit = SubmitField('Add')