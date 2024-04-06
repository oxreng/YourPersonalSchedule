from flask import Flask, render_template


app = Flask(__name__)


@app.route('/calendar')
def calendar_mouth():
    return render_template('html/calendar.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)