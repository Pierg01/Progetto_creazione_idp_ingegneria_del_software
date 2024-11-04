import os.path

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, template_folder='../templates',static_folder='../static')



@app.route('/')
def mainpage():
    if request.method == "GET":
        return render_template('index.html')


    




@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registrazione')
def registrazione():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)