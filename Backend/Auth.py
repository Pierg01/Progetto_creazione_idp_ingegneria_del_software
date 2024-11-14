import requests
import oauthlib.oauth2 as oauth2
from flask import Flask, render_template, request, redirect, url_for
from jwt import PyJWT
from oauthlib.common import generate_client_id
from oauthlib.oauth2 import BackendApplicationClient
import jwt
import Utente
import autorization

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def mainpage():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        print("RICHIESTA POST")
        username = request.form['username']
        password = request.form['password']
        utente = Utente.Utente("", "")
        utente.search({'username': username, 'password': password})
        print("Ingresso if")
        if utente.compare_password(utente.password):
            print("Sono entrato nella if")
            jwtt = PyJWT()
            token = jwtt.encode(payload={"Username": utente.Username, "Password": utente.password}, key="secret",
                               algorithm='HS256')
            return redirect(url_for("token_generator", strtoken=token))
        return render_template('login.html')

@app.route('/token_generator', methods=['GET', 'POST'])
def otp_code():
    if request.method=="POST":
        metodo=request.form['2FA_chose']
        if metodo=="TOTP":
            codice=request.form['code']
            if autorization.totp_generatore.verify_totp(codice):
                return True
            else:
                return False
        elif metodo=="EMAIL":
            codice = request.form['code']
            #continua con 2FA via email



@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == "GET":
        return render_template('register.html')


@app.route('/token', methods=['GET'])
def token_generator():
    token = request.args.get('strtoken')
    if request.method == "GET":
        return render_template('token_generator.html', strtoken=token)

if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"

    app.run(port=3000, debug=True)
