from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'


@app.route('/')
def main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')