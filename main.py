from flask import Flask, render_template, redirect
from data.database import db_session
from forms.login import LoginForm
from forms.register import RegisterForm
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from data.database.users import User
from data.database.notes import Note
from datetime import datetime
import locale

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MICHAEL_JORDAN_THE_BEST'

db_session.global_init('data/database/app.sqlite')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/calendar')
def calendar_month():
    return render_template('calendar.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/notes')
@login_required
def notes():
    session = db_session.create_session()
    notes = session.query(Note).filter(Note.user_id == current_user.id).all()
    for note in notes:
        note.datetime = note.datetime.strftime("%Y/%m/%d")
        note.datetime = note.datetime.split()
        note.datetime[0] = datetime.strptime(note.datetime[0], "%Y/%m/%d").strftime("%B %d, %Y")
        note.datetime = ' '.join(note.datetime)
    return render_template('notes.html', notes=notes)


@app.route('/edit_note')
def edit_note():
    return render_template('main_page.html')


@app.route('/delete_note')
def delete_note():
    return render_template('main_page.html')


@app.route('/add_note')
def add_note():
    return render_template('main_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message='Пароли в обоих полях должны совпадать')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message=f'Электронная почта {form.email.data} уже используется')
        user = User(
            name=form.name.data,
            email=form.email.data,
            bday=form.bday.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               form=form,
                               message='Неверный логин или пароль')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
