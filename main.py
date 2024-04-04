import datetime

from flask import Flask, render_template
from data.database import db_session
from data.database.users import Users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MICHAEL_JORDAN_THE_BEST'

db_session.global_init('data/database/app.sqlite')

db_sess = db_session.create_session()


@app.route('/')
def main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
