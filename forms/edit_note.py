from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditNoteForm(FlaskForm):
    edit_title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    edit_content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=1000)])
