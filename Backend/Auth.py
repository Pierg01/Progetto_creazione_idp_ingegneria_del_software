import json
import smtplib
import Token
from flask import Flask, render_template, request, redirect, url_for
import Utente
import autorization
import string
import random
import base64

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
        username = request.form['username']
        password = request.form['password']
        prova_utente = {"Username": username, "Password": password}
        utente = Utente.search_user(prova_utente["Username"])
        if not utente:
            return redirect(url_for('login'))

        if Utente.compare_password(prova_utente["Password"], utente["Password"]):
            catatteri = string.ascii_lowercase

            iid = 'b'.join(random.choice(catatteri) for _ in range(5))+base64.b64encode(utente["Username"].encode('utf-8')).decode('utf-8')


            return redirect(url_for('otp_code', iid=iid))
        else:

            return redirect(url_for('login'))

@app.route('/otp_code/<iid>', methods=['POST', 'GET'])
def otp_code(iid):
    if request.method == "GET":
        return render_template('token_generator.html', iid=iid)
    elif request.method == "POST":



        username=base64.b64decode(iid[9:len(iid)]).decode('utf-8')



        utente = Utente.search_user(username)
        key = utente.get("chiave segreta")
        metodo = request.form['2FA_chose']
        if metodo == "TOTP":
            codice = request.form['code']
            if autorization.verify_totp(key, codice):
                return open(Token.send_request_token(utente).json()[0])
            else:
                return "Codice non valido", 400
        elif metodo == "EMAIL":
            #codice per inviare la mail
            codice = request.form['code']
            # codice per verificare se il codice inserito è corretto

@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == "GET":
        return render_template('register.html')
    # Acquisisco i dati del nuovo utente dal form
    user = request.form['username']
    password = request.form['password']
    email = request.form['email']
    chiave = autorization.generate_key()
    uri = autorization.generate_uri(chiave, user, email)
    qr_code_img = autorization.generate_qrcode(uri)
    # Verifico che l'utente non sia già registrato
    if Utente.search_user(user)["Username"] is None:
        utente = {
            "Username": user,
            "Password": password,
            "Email": email,
            "chiave segreta": chiave
        }
        #verifica dell'esistenza della email
        # Inserisco l'utente nel database e genero il QR code per il TOTP
        Utente.insert_user(utente)
        return render_template('show_qrcode.html', qr_code_img=qr_code_img, username=user)


# Verifica del codice TOTP
@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    username = request.form['username']
    code = request.form['code']
    utente = Utente.search_user(username)
    key = utente["chiave segreta"]

    if autorization.verify_totp(key, code):
        return render_template('success.html')
    else:
        token = request.form['token']  # Ensure token is retrieved from the form
        return render_template('insuccess.html', token=token)


@app.route('/recupero_mail',methods=['POST'])
def recupero_mail(iid):



if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"
    app.run(port=3000, debug=True)
