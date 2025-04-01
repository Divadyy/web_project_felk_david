import os
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return redirect('/catalog')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/temp')
def temp():
    return render_template('temp.html')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8080)
    app.run(host='0.0.0.0', port=port)
