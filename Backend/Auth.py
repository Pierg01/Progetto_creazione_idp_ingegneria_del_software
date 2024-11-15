import requests
from flask import Flask, render_template, request, redirect, url_for
from jwt import PyJWT
from pycparser.ply.yacc import token
from urllib3.util import SSLContext
import json

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
        print("Richiesta post")
        username = request.form['username']
        password = request.form['password']
        prova_utente={"Username": username, "Password": password}
        utente = Utente.search_user(prova_utente["Username"])
        print(utente)

        if Utente.compare_password(prova_utente["Password"], utente["Password"]):
            jwt = PyJWT()
            jwtt = jwt.encode(payload={"Username": utente["Username"], "Password": utente["Password"]}, key="secret",algorithm="HS256")
            return redirect(url_for('otp_code',token=jwtt))
        else:
            print(False)
            return redirect(url_for('login'))

@app.route('/registrazione', methods=['GET', 'POST'])
# registrazione utente
# verificare che nome utente sia unico,
# Verificare che la password sia abbastanza lunga e contenga determinati caratteri
#
def registrazione():
    if request.method == "GET":
        return render_template('register.html')

    user = request.form['username']
    password = request.form['password']
    email = request.form['email']
    chiave = autorization.generate_uri(autorization.generate_key(),user,email)
    if Utente.search_user(user)["Username"] is None:
        utente = {
            "Username": user,
            "Password": password,
            "Email": email,
            "chiave segreta": chiave
        }
        Utente.insert_user(utente)
        return redirect(url_for('login'))

@app.route('/otp_code',methods=['POST'])
def otp_code(token: str):
    jwt = PyJWT()
    utente = PyJWT.decode(jwt,token,key="secret",algorithm="HS256")
    username = utente["Username"]

    utente = Utente.search_user(username)
    key = utente.get("chiave_segreta")
    email = utente.get("email")
    uri = autorization.generate_uri(key,utente.get("Username"),email)
    if request.method=="POST":
        metodo=request.form['2FA_chose']
        if metodo=="TOTP":
            codice=request.form['code']
            if autorization.verify_totp(key,codice):
                print(True)
                return True
            else:
                return False
        elif metodo=="EMAIL":
            codice = request.form['code']
            #continua con 2FA via email


if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"

    app.run(port=3000, debug=True)
