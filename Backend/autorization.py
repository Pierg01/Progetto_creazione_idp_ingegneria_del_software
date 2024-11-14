import pyotp
import qrcode



def generate_key():
    return pyotp.random_base32()

def generate_uri(key,username,email):
    return pyotp.totp.TOTP(key).provisioning_uri(name=username, issuer_name=email)

def generate_qrcode(uri):
    return qrcode.make(uri)

        # metodo di verifica del totp
def verify_totp(key,codice) -> bool:
    return pyotp.TOTP(key).verify(codice)





#se il return è vero allora
#return render_template('index.html')

#se è falso
#return render_template('login.html')
#prova pull