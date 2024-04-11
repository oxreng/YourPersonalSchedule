from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length
from datetime import date


class AddNoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=255)])
    content = TextAreaField('Текст', validators=[DataRequired(), Length(min=1, max=10000)])
    date = DateField('Дата заметки', default=date.today, validators=[DataRequired()])
