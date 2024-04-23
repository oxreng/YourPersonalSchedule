from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired
import datetime as dt


class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content')
    start_date = DateField('Start Date', validators=[DataRequired()],
                           default=dt.datetime.now().date())
    start_time = TimeField('Start Time', validators=[DataRequired()],
                           default=dt.datetime.now().time())
    end_date = DateField('End Date', validators=[DataRequired()],
                         default=dt.datetime.now().date())
    end_time = TimeField('End Time', validators=[DataRequired()],
                         default=dt.time(23, 59, 59))
    submit = SubmitField('Add')
