import jwt
import requests

def send_request_token(utente: dict):
    jwtt = jwt.PyJWT()
    token = jwtt.encode(payload={"Username": utente["Username"], "Password": utente["Password"]}, key="secret",
                        algorithm='HS256')[0]
    requests.get("", headers={"Authorization": "Bearer" + token}, allow_redirects=False)