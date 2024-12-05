import base64
import json
import random
import string
import time

import requests
from flask import Flask, render_template, request, redirect, url_for
from pymongo.response import Response

import Utente
import autorization
import verifica_email
from Backend import Token

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
            iid = 'b'.join(random.choice(catatteri) for _ in range(5)) + base64.b64encode(
                utente["Username"].encode('utf-8')).decode('utf-8')
            return redirect(url_for('otp_code', iid=iid))
        else:
            return redirect(url_for('login'))


@app.route('/otp_code/<iid>', methods=['POST', 'GET'])
def otp_code(iid):
    if request.method == "GET":
        return render_template('token_generator.html', iid=iid)
    elif request.method == "POST":
        username = base64.b64decode(iid[9:len(iid)]).decode('utf-8')
        utente = Utente.search_user(username)
        key = utente.get("chiave segreta")
        metodo = request.form['2FA_chose']
        if metodo == "TOTP":
            codice = request.form['code']
            if autorization.verify_totp(key, codice):
                return open(Token.send_request_token(utente).json()[0])
            else:
                return "Codice non valido", 400



@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == "GET":
        return render_template('register.html')

    # Acquisisco i dati del nuovo utente dal form
    user = request.form['username']
    password = request.form['password']
    email = request.form['email']

    #Verifico che il nome utente sia nei limiti di caratteri e senza spazi
    if len(user) < 3 or len(user) > 25:
        return render_template('register.html', error="Username deve contenere minimo 3 e al massimo 25 caratteri.")
    if any(char in string.punctuation for char in user) or " " in user:
        return render_template('register.html', error="Username non deve contenere caratteri speciali o spazi")

    # verifico se utente inserisce una password corretta con almeno 8 caratteri, un numero e non caratteri speciali
    if user == password:
        return render_template('register.html', error="Username e password non possono coincidere.")
    if len(password) < 8 or len (password) > 128:
        return render_template('register.html', error=" password deve essere minimo 8 caratteri.")
    if not any(char.isupper() for char in password) or  not any(char.isdigit() for char in password):
        return render_template('register.html', error="La password deve contenere almeno un carattere maiuscolo e un numero")
    if any(char in string.punctuation for char in password)  or " " in password:
        return render_template('register.html', error="Password non deve contenere caratteri speciali o spazi")



    # Verifico se l'email è valida
    print(f"Verifying email: {email}")
    is_email_valid, message = verifica_email.verify_email_smtp(email)
    print(f"Email valid: {is_email_valid}, Message: {message}")
    if not is_email_valid:
        return render_template('register.html', error=f"Errore email: {message}")
    print("Email verificata correttamente.")
    # Genero chiave segreta e URI per il TOTP
    chiave = autorization.generate_key()
    uri = autorization.generate_uri(chiave, user, email)
    qr_code_img = autorization.generate_qrcode(uri)

    # Verifico che l'utente non sia già registrato
    if not Utente.search_user(user):
        print("Ho verificato se l'utente esiste")
        utente = {
            "Username": user,
            "Password": password,
            "Email": email,
            "chiave segreta": chiave
        }
        # Inserisco l'utente nel database e genero il QR code per il TOTP
        Utente.insert_user(utente)
        return render_template('show_qrcode.html', qr_code_img=qr_code_img, username=user)
    else:
        # Se l'utente esiste già, segnalo errore
        return render_template('register.html', error="Utente già registrato.")


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
        return "Codice non valido", 400


@app.route('/inserimento/<iid>', methods=['GET', 'POST'])
def inserimento(iid):
    if request.method == 'GET':
        utente = Utente.search_user(base64.b64decode(iid[9:len(iid)]).decode('utf-8'))
        email = utente["Email"]
        cod_gen = autorization.generate_code(utente["chiave segreta"])
        verifica_email.invia_mex(email, cod_gen)
        return render_template('inserimento_codice.html', iid=iid, cod_gen=cod_gen)


@app.route('/verifica_codice/<iid>/<cod_gen>', methods=['POST'])
def verifica_codice(iid, cod_gen):
    if request.method == 'POST':
        codice = request.form['codice']
        if cod_gen == codice:
            utente = Utente.search_user(base64.b64decode(iid[9:len(iid)]).decode('utf-8'))
            chiave = utente["chiave segreta"]
            email = utente["Email"]
            user = utente["Username"]
            uri = autorization.generate_uri(chiave, user, email)
            qr_code_img = autorization.generate_qrcode(uri)
            return render_template('qr_code_recuperato.html', qr_code_img=qr_code_img, username=user)
        else:
            return "Codice errato", 400
    return "Invalid request method", 405


@app.route('/verify_totp_recuperato', methods=['POST'])
def verify_totp_recuperato():
    username = request.form['username']
    code = request.form['code']
    utente = Utente.search_user(username)
    key = utente["chiave segreta"]
    if autorization.verify_totp(key, code):
        return render_template('recuperato_success.html')
    else:
        return "Codice non valido", 400


@app.route('/send_email/<iid>', methods=['POST'])
def send_email(iid):
    if request.method == 'POST':
        utente = Utente.search_user(base64.b64decode(iid[9:len(iid)]).decode('utf-8'))
        counter = int(time.time() // 30)  # Example counter based on time
        cod_gen = autorization.generate_hotp(utente["chiave segreta"], counter)
        verifica_email.invia_mex(utente["Email"], cod_gen)
        return redirect(url_for('step_finale_email', iid=iid))

@app.route('/step_finale_email/<iid>', methods=['GET', 'POST'])
def step_finale_email(iid):
    if request.method == 'GET':
        return render_template('Verifica_codice_email.html', iid=iid)
    if request.method == 'POST':
        user = base64.b64decode(iid[9:len(iid)]).decode('utf-8')
        utente = Utente.search_user(user)
        code = request.form['code']
        counter = int(time.time() // 30)  # Example counter based on time
        expected_code = autorization.generate_hotp(utente["chiave segreta"], counter)
        if expected_code == code:
            return 'codice corretto', 200
        else:
            return 'codice errato', 400

if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"
    app.run(port=3000, debug=True)