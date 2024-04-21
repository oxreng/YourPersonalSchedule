from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    bday = DateField('День рождения')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Создать аккаунт')
