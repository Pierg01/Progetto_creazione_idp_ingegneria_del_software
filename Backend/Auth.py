import base64
import datetime
import hashlib
import random
import string
import time
from flask import Flask, render_template, request, redirect, url_for
from jwt import PyJWT
import Utente
import autorization
import verifica_email
app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Caricamento pagina iniziale
@app.route('/')
def mainpage():
    if request.method == "GET":
        return render_template('index.html')



# Route di gestione del login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        predefined_salt = '10'
        # Hash the password with the predefined salt
        psw = hashlib.sha256((predefined_salt + password).encode('utf-8')).hexdigest()
        prova_utente = {"Username": username, "Password": psw}
        utente = Utente.search_user(prova_utente["Username"])
        if not utente:
            return render_template('login.html', error="Utente inesistente, "
                                                       "cliccare in basso per registrarsi")

        psw1=prova_utente["Password"]
        psw2=utente["Password"]
        if Utente.compare_password(psw1, psw2):
            caratteri = string.ascii_lowercase
            iid = 'b'.join(random.choice(caratteri) for _ in range(5)) + base64.b64encode(
                utente["Username"].encode('utf-8')).decode('utf-8')
            return redirect(url_for('otp_code', iid=iid))
        else:
            return render_template('login.html', error="Password errata")


# Login con 2FA mediante TOTP
@app.route('/otp_code/<iid>', methods=['POST', 'GET'])
def otp_code(iid):
    if request.method == "GET":
        return render_template('token_generator.html', iid=iid)
    elif request.method == "POST":
        return redirect(url_for('step_finale_totp', iid=iid))


@app.route('/step_finale_totp/<iid>/', methods=['GET', 'POST'])
def step_finale_totp(iid):
    if request.method == 'GET':
        return render_template("Verifica_codice_totp.html", iid=iid)
    elif request.method == 'POST':
        utente = Utente.search_user(base64.b64decode(iid[9:len(iid)]).decode('utf-8'))
        chiave = utente["chiave segreta"]
        code = request.form["code"]
        if autorization.verify_totp(chiave, code):
            key = Utente.get_key_token(utente)
            jwtt = PyJWT()
            token = jwtt.encode(payload={"Username":utente["Username"],"exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(minutes=1)},key=key,algorithm="HS256")
            key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
            return redirect(f"http://localhost:2000/{ token }/{key}")
        else:
            return render_template("Verifica_codice_totp.html", iid=iid, error="Codice errato, riprova"
                                                                               " o recupera chiave TOTP dal link in basso")


# Route per login con 2FA mail
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
        print(utente)
        code = request.form['code']
        counter = int(time.time() // 30)  # Example counter based on time
        expected_code = autorization.generate_hotp(utente["chiave segreta"], counter)
        if expected_code == code or autorization.generate_hotp(utente["chiave segreta"],
                                                  counter - 1) == code or autorization.generate_hotp(
                utente["chiave segreta"], counter + 1) == code:
            key = Utente.get_key_token(utente)
            jwtt = PyJWT()
            token = jwtt.encode(payload={"Username":utente["Username"],"exp": (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=1)).timestamp()},key=key,algorithm="HS256")
            key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
            return redirect(f"http://localhost:2000/{token}/{key}")
        else:
            return render_template('Verifica_codice_email.html', iid=iid, error="Codice non valido. Riprova.")


# Route per la gestione della registrazione
@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == "GET":
        return render_template('register.html')
    # Acquisisco i dati del nuovo utente dal form
    user = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Verifico che il nome utente sia nei limiti di caratteri e senza spazi
    if len(user) < 3 or len(user) > 25:
        return render_template('register.html', error="Username deve contenere minimo 3 e al massimo 25 caratteri.")
    if any(char in string.punctuation for char in user) or " " in user:
        return render_template('register.html', error="Username non deve contenere caratteri speciali o spazi")

    # verifico se utente inserisce una password corretta con almeno 8 caratteri, un numero e non caratteri speciali
    if user == password:
        return render_template('register.html', error="Username e password non possono coincidere.")
    if len(password) < 8 or len(password) > 128:
        return render_template('register.html', error=" password deve essere minimo 8 caratteri.")
    if not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
        return render_template('register.html',
                               error="La password deve contenere almeno un carattere maiuscolo e un numero")
    if any(char in string.punctuation for char in password) or " " in password:
        return render_template('register.html', error="Password non deve contenere caratteri speciali o spazi")

    # Verifico se l'email è valida
    is_email_valid, message = verifica_email.verify_email_smtp(email)
    if not is_email_valid:
        return render_template('register.html', error=f"Errore email: {message}")
    # Genero chiave segreta e URI per il TOTP
    chiave = autorization.generate_key()
    uri = autorization.generate_uri(chiave, user, email)
    qr_code_img = autorization.generate_qrcode(uri)
    predefined_salt = '10'
    # Hash the password with the predefined salt
    psw = hashlib.sha256((predefined_salt + password).encode('utf-8')).hexdigest()
    # Verifico che l'utente non sia già registrato
    if not Utente.search_user(user):
        utente = {
            "Username": user,
            "Password": psw,
            "Email": email,
            "chiave segreta": chiave,
            "Key token": ""
        }
        # Inserisco l'utente nel database e genero il QR code per il TOTP
        Utente.insert_user(utente)
        return render_template('show_qrcode.html', qr_code_img=qr_code_img, username=user)
    else:
        # Se l'utente esiste già, segnalo errore
        return render_template('register.html', error="Utente già registrato.")


# Route per la configurazione della 2FA con TOTP per l'utente
@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    username = request.form['username']
    code = request.form['code']
    utente = Utente.search_user(username)
    key = utente["chiave segreta"]
    uri=autorization.generate_uri(key, username, utente["Email"])
    img=autorization.generate_qrcode(uri)
    if autorization.verify_totp(key, code):
        return render_template('success.html')
    else:
        return render_template('show_qrcode.html', error="Codice non valido", qr_code_img=img, username=username)


# Route per la gestione del recupero della chiave TOTP in caso di perdita
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
            return render_template('inserimento_codice.html', iid=iid, cod_gen=cod_gen, error="Codice errato")
    return "Invalid request method", 405


@app.route('/verify_totp_recuperato', methods=['POST'])
def verify_totp_recuperato():
    username = request.form['username']
    code = request.form['code']
    utente = Utente.search_user(username)
    key = utente["chiave segreta"]
    uri = autorization.generate_uri(key, username, utente["Email"])
    img = autorization.generate_qrcode(uri)
    if autorization.verify_totp(key, code):
        return render_template('recuperato_success.html')
    else:
        return render_template('qr_code_recuperato.html', error="Codice non valido", username=username, qr_code_img=img)


@app.route('/refresh_token/{{ token }}/{{ key }}',methods=["POST"])
def refresh_token(token,key):


    jwtt = PyJWT()
    utente =jwtt.decode(token,key=key,algorithms=["HS256"])

    token = jwtt.encode(payload={"Username": utente["Username"],
                                 "exp": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)).timestamp()},
                        key=key, algorithm="HS256")
    key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
    return redirect(f"http://localhost:2000/{token}/{key}")



if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"
    app.run(port=3000, debug=True)