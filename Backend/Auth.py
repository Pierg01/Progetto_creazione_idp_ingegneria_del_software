import oauthlib.oauth2 as oauth2
from authlib.common.urls import url_encode

from flask import Flask, render_template, request, redirect, url_for

from Backend.Utente import Utente

app = Flask(__name__, template_folder='../templates',static_folder='../static')



@app.route('/')
def mainpage():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/login')
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        utente= Utente("","")
        if utente.search({"username":username,"password":password}) is not None:
            if utente.compare_password(password):
                oauth2.BackendApplicationClient.prepare_request_body(url_encode({"username":username,"password":password}))








        


@app.route('/registrazione')
def registrazione():
    if request.method == "GET":
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)