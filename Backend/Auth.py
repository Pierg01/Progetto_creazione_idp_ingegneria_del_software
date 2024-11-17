from flask import Flask, render_template, request, redirect, url_for
from jwt import PyJWT

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
        # Acquisisco i dati dal form
        username = request.form['username']
        password = request.form['password']
        prova_utente = {"Username": username, "Password": password}

        # Cerco l'utente nel database
        utente = Utente.search_user(prova_utente["Username"])
        # Se l'utente non esiste, ritorno alla pagina di login
        if utente is None:
            print("Utente non trovato")
            return redirect(url_for('login'))

        print("Utente trovato:", utente)

        # Verifico la correttezza della password
        if Utente.compare_password(prova_utente["Password"], utente["Password"]):
            jwt = PyJWT()
            jwtt = jwt.encode(payload={"Username": utente["Username"], "Password": utente["Password"]}, key="secret",
                              algorithm="HS256")
            print("JWT generato:", jwtt)
            return redirect(url_for('token_generator', strtoken=jwtt))
        else:
            print("Password errata")
            return redirect(url_for('login'))


@app.route('/token_generator')
def token_generator():
    strtoken = request.args.get('strtoken')
    return render_template('token_generator.html', strtoken=strtoken)


@app.route('/registrazione', methods=['GET', 'POST'])
# registrazione utente

# Verificare che la password sia abbastanza lunga e contenga determinati caratteri
#
def registrazione():
    if request.method == "GET":
        return render_template('register.html')
#Acquisisco i dati del nuovo utente dal form
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
        # Inserisco l'utente nel database e genero il QR code per il TOTP
        Utente.insert_user(utente)
        return render_template('show_qrcode.html', qr_code_img=qr_code_img, username=user)

#Verifica del codice TOTP
@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    username = request.form['username']
    code = request.form['code']
    utente = Utente.search_user(username)
    key = utente["chiave segreta"]

    if autorization.verify_totp(key, code):
        return redirect(url_for('login'))
    else:
        return "Codice TOTP non valido. Riprova.", 400

@app.route('/acquisisci_metodo/<token>', methods=['POST'])
def acquisisci_metodo():
    jwt = PyJWT()
    utente = jwt.decode(token, key="secret", algorithms=["HS256"])
    username = utente["Username"]

    utente = Utente.search_user(username)
    key = utente.get("chiave_segreta")
    email = utente.get("email")
    uri = autorization.generate_uri(key, utente.get("Username"), email)

    metodo = request.form["2FA_chose"]
    return metodo
@app.route('/otp_code/<token>', methods=['POST'])
def otp_code(token: str):
    metodo=acquisisci_metodo()
    if metodo == "TOTP":
        codice = request.form.get('codeInput')
        if autorization.verify_totp(key, codice):
            return "TOTP verification successful", 200
        else:
            return "TOTP verification failed", 400
    elif metodo == "EMAIL":
        codice = request.form.get('codeInput')
        # continua con 2FA via email
        return "Email verification not implemented", 501
    else:
        return "Invalid 2FA method", 400


if __name__ == '__main__':
    FLASK_APP = "./Backend/Auth.py"

    app.run(port=3000, debug=True)
