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
        username = request.form['username']
        password = request.form['password']
        prova_utente={"Username": username, "Password": password}
        utente = Utente.search_user(prova_utente)
        print(utente)

        if Utente.compare_password(prova_utente["Password"], utente["Password"]):
            jwtt = PyJWT()
            token = jwtt.encode(payload={"Username": utente["Username"], "Password":utente["Password"]}, key="secret",algorithm='HS256')
            return redirect(url_for("token_generator", strtoken=token))
        else:
            print(False)
            return redirect(url_for("login"))

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
