from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from flask_login import current_user
from data.database.users import User
from data.database import db_session


# pip install email_validator
# pip install Pillow
class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            session = db_session.create_session()
            user = session.query(User).filter(User.email == email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
