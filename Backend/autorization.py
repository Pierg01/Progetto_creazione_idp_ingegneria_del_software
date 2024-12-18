import base64
import hashlib
import hmac
import string
import struct
from io import BytesIO
from operator import truediv

import pyotp
import qrcode
from flask import render_template


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

def generate_hotp(secret, counter):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    o = hmac_hash[19] & 15
    hotp = (struct.unpack(">I", hmac_hash[o:o+4])[0] & 0x7fffffff) % 1000000
    return '{:06d}'.format(hotp)
