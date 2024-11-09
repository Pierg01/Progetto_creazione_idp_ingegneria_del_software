import requests
import oauthlib.oauth2 as oauth2
from flask import Flask, render_template, request, redirect, url_for
from oauthlib.common import generate_client_id
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.openid.connect.core.tokens import JWTToken

from Backend.Utente import Utente

app = Flask(__name__, template_folder='../templates',static_folder='../static')



@app.route('/')
def mainpage():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        utente = Utente("","")
        utente.search({'username':username,'password':password})
        if utente.compare_password(password):
            print(utente.compare_password(password))
            token = JWTToken(request_validator=utente.compare_password(password))

            token.create_token(utente,refresh_token=True)
            return requests.get("",params={"token": token})
    return redirect(url_for('login'))















@app.route('/registrazione')
def registrazione():
    if request.method == "GET":
        return render_template('register.html')

@app.route('/token',methods=['GET'])
def token_generator():
    if request.method == "GET":
        return render_template('token_generator.html')

if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"

    app.run(debug=True)