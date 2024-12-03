import pyotp
import qrcode
import base64
from io import BytesIO

def generate_key():
    return pyotp.random_base32()

def generate_uri(key, username, email):
    return pyotp.totp.TOTP(key).provisioning_uri(name=username, issuer_name=email)

def generate_qrcode(uri):
    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def verify_totp(key,codice) -> bool:
    return pyotp.TOTP(key).verify(codice)

def generate_code(key):
    return pyotp.TOTP(key).now()