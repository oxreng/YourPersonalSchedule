from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.database import db_session
from forms.login import LoginForm
from forms.register import RegisterForm
from flask_login import login_required, login_user, logout_user, current_user
from data.database.users import User
from data.database.notes import Note
from data.database.calendar import Calendar
from datetime import datetime, timedelta
from forms.addnote import AddNoteForm
from forms.edit_note import EditNoteForm
from forms.event import EventForm

user_blueprint = Blueprint('user_views', __name__, template_folder='templates')


@user_blueprint.route('/')
def static():
    return redirect(url_for('user_views.main_page'))


@user_blueprint.route('/main_page')
def main_page():
    return render_template('main_page.html')


@user_blueprint.route('/calendar')
@login_required
def calendar():
    session = db_session.create_session()
    events_db = session.query(Calendar).filter(Calendar.user_id == current_user.id).all()
    events = []
    for event in events_db:
        events.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.strftime("%Y-%m-%d"),
            'end': (event.end + timedelta(days=1)).strftime("%Y-%m-%d")
        })
    return render_template('calendar.html', events=events)


@user_blueprint.route('/calendar_add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        session = db_session.create_session()
        new_event = Calendar(
            title=form.title.data,
            start=form.start.data,
            end=form.end.data,
            user_id=current_user.id
        )
        session.add(new_event)
        session.commit()

        return redirect(url_for('user_views.calendar'))
    return render_template('add_event.html', form=form)


@user_blueprint.route('/calendar_edit_event/<event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    form = EventForm(request.form)
    session = db_session.create_session()
    event = session.query(Calendar).filter(event_id == Calendar.id).first()
    event.start = event.start.strftime("%Y-%m-%d")
    event.end = event.end.strftime("%Y-%m-%d")
    if request.method == 'POST' and form.validate_on_submit():
        event.title = form.title.data
        event.start = form.start.data
        event.end = form.end.data
        session.commit()
        return redirect(url_for('user_views.calendar'))
    return render_template('edit_event.html', form=form, event=event)


@user_blueprint.route('/calendar_delete_event/<event_id>', methods=['GET'])
@login_required
def delete_event(event_id):
    session = db_session.create_session()
    event = session.query(Calendar).filter(event_id == Calendar.id).first()
    session.delete(event)
    session.commit()
    flash("Event deleted 🗑️", category='success')
    return redirect(url_for('user_views.calendar'))


@user_blueprint.route('/schedule')
def schedule():
    return render_template('schedule.html')


@user_blueprint.route('/notes', methods=['GET'])
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


@user_blueprint.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = AddNoteForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        session = db_session.create_session()
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            datetime=form.date.data,
            user_id=current_user.id
        )
        session.add(new_note)
        session.commit()
        flash('Заметка добавлена ✅', category='success')
        return redirect(url_for('user_views.notes'))

    return render_template('add_note.html', form=form)


@user_blueprint.route('/edit_note/<note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    form = EditNoteForm(request.form)
    session = db_session.create_session()
    note = session.query(Note).filter(note_id == Note.note_id).first()
    if request.method == 'POST' and form.validate_on_submit():
        note.title = form.edit_title.data
        note.content = form.edit_content.data
        session.commit()
        flash("Note updated 👍", category='success')
        return redirect(url_for('user_views.notes'))
    return render_template('edit_note.html', form=form, note=note)


@user_blueprint.route('/delete_note/<note_id>', methods=['GET'])
@login_required
def delete_note(note_id):
    session = db_session.create_session()
    note = session.query(Note).filter(note_id == Note.note_id).first()
    session.delete(note)
    session.commit()
    flash("Note deleted 🗑️", category='success')
    return redirect(url_for('user_views.notes'))


@user_blueprint.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('user_views.main_page'))
    return render_template('register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('user_views.main_page'))
        return render_template('login.html',
                               form=form,
                               message='Неверный логин или пароль')
    return render_template('login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_views.main_page'))
