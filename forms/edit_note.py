from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditNoteForm(FlaskForm):
    edit_title = StringField('Название', validators=[DataRequired(), Length(min=1, max=255)])
    edit_content = TextAreaField('Текст', validators=[DataRequired(), Length(min=1, max=10000)])
