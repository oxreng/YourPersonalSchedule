from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from data.database import db_session
from forms.login import LoginForm
from forms.register import RegisterForm
from flask_login import login_required, login_user, logout_user, current_user
from data.database.users import User
from data.database.notes import Note
from data.database.calendar import Calendar
from datetime import datetime, timedelta
from forms.add_note import AddNoteForm
from forms.edit_note import EditNoteForm
from forms.add_task import AddTaskForm
from data.database.tasks import Task
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
        flag = ''
        end = event.end_date
        if (event.start_date == event.end_date and str(event.start_time) == '00:00:00'
                and str(event.end_time) == '23:59:00' or (event.end_date - event.start_date).days > 1):
            flag = 1
            end = event.end_date + timedelta(days=1)
        events.append({
            'id': event.id,
            'title': event.title,
            'start': f'{event.start_date}T{event.start_time}',
            'end': f'{end}T{event.end_time}',
            'color': event.color,
            'duration': flag
        })
    return render_template('calendar.html', events=events)


@user_blueprint.route('/calendar_add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm(request.form)
    session = db_session.create_session()
    if request.method == 'POST' and form.validate_on_submit():
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(form.end_date.data, form.end_time.data)
        if start > end:
            message = 'End date should be later than start date'
            return render_template('edit_event.html', form=form, message=message)
        new_event = Calendar(
            title=form.title.data,
            start_date=form.start_date.data,
            start_time=form.start_time.data,
            end_date=form.end_date.data,
            end_time=form.end_time.data,
            user_id=current_user.id,
            color=form.color.data
        )
        session.add(new_event)
        session.commit()
        flash('Event added ✅', category='success')

        return redirect(url_for('user_views.calendar'))
    return render_template('add_event.html', form=form)


@user_blueprint.route('/calendar_edit_event/<event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    form = EventForm(request.form)
    session = db_session.create_session()
    event = session.query(Calendar).filter(event_id == Calendar.id).first()
    if request.method == 'POST':
        start_time, end_time = event.start_time, event.end_time

        if form.start_time.data:
            start_time = form.start_time.data
        if form.end_time.data:
            end_time = form.end_time.data

        start = datetime.combine(form.start_date.data, start_time)
        end = datetime.combine(form.end_date.data, end_time)
        if start > end:
            message = 'End date should be later than start date'
            return render_template('edit_event.html', form=form, event=event, message=message)
        event.title = form.title.data
        event.start_date = form.start_date.data
        event.start_time = start_time
        event.end_date = form.end_date.data
        event.end_time = end_time
        event.color = form.color.data

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


@user_blueprint.route('/tasks')
@login_required
def tasks():
    session = db_session.create_session()
    active_tasks = sorted(session.query(Task).filter(Task.active == True and Task.user_id == current_user.id).all(),
                          key=lambda x: x.date_start)
    inactive_tasks = sorted(session.query(Task).filter(Task.active == False and Task.user_id == current_user.id).all(),
                            key=lambda x: x.date_start)
    for task in active_tasks:
        task.date_start = task.date_start.strftime("%Y/%m/%d")
        task.date_end = task.date_end.strftime("%Y/%m/%d")
        task.time_start = task.time_start.strftime("%H:%M")
        task.time_end = task.time_end.strftime("%H:%M")
    for task in inactive_tasks:
        task.date_start = task.date_start.strftime("%Y/%m/%d")
        task.date_end = task.date_end.strftime("%Y/%m/%d")
        task.time_start = task.time_start.strftime("%H:%M")
        task.time_end = task.time_end.strftime("%H:%M")
    return render_template('tasks.html', active_tasks=active_tasks, inactive_tasks=inactive_tasks)


@user_blueprint.route('/change_task_state/<int:task_id>')
def change_task_state(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if task.active is True:
        task.active = False
    else:
        task.active = True
    session.commit()
    return redirect('/tasks')


@user_blueprint.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if datetime.now().date() > form.end_date.data:
            return render_template('add_task.html',
                                   form=form,
                                   message='End date should be later than present')
        if form.start_date.data > form.end_date.data:
            return render_template('add_task.html',
                                   form=form,
                                   message='End date should be later than start date')
        if len(form.title.data) > 25:
            return render_template('add_task.html',
                                   form=form,
                                   message='Title length should be under 25 characters.')
        if len(form.content.data) > 100:
            return render_template('add_task.html',
                                   form=form,
                                   message='Content length should be under 100 characters.')
        task = Task(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            date_start=form.start_date.data,
            date_end=form.end_date.data,
            time_start=form.start_time.data,
            time_end=form.end_time.data
        )
        session.add(task)
        session.commit()
        flash('Task added ✅', category='success')
        return redirect('/tasks')
    return render_template('add_task.html', form=form)


@user_blueprint.route('/edit_task/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    form = AddTaskForm()
    session = db_session.create_session()
    if request.method == 'GET':
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            form.title.data = task.title
            form.content.data = task.content if task.content else ''
            form.start_date.data = task.date_start
            form.start_time.data = task.time_start
            form.end_date.data = task.date_end
            form.end_time.data = task.time_end
        else:
            abort(404)
    if request.method == 'POST':
        if form.validate_on_submit():
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                if datetime.now().date() > form.end_date.data:
                    return render_template('add_task.html',
                                           form=form,
                                           message='End date should be later than present')
                if form.start_date.data > form.end_date.data:
                    return render_template('add_task.html',
                                           form=form,
                                           message='End date should be later than start date')
                if len(form.title.data) > 25:
                    return render_template('add_task.html',
                                           form=form,
                                           message='Title length should be under 25 characters.')
                if len(form.content.data) > 100:
                    return render_template('add_task.html',
                                           form=form,
                                           message='Content length should be under 100 characters.')
                task.title = form.title.data
                task.content = form.content.data
                task.date_start = form.start_date.data
                task.time_start = form.start_time.data
                task.date_end = form.end_date.data
                task.time_end = form.end_time.data
                session.commit()
                flash("Task updated 👍️", category='success')
                return redirect('/tasks')
            abort(404)
    return render_template('add_task.html', form=form)


@user_blueprint.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == task_id).first()
    session.delete(task)
    session.commit()
    flash("Task deleted 🗑️", category='success')
    return redirect('/tasks')


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
        flash('Note added ✅', category='success')
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
                               message='Invalid username or password')
    return render_template('login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_views.main_page'))
