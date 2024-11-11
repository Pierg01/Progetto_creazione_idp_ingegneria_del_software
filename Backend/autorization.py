import pyotp
import qrcode

class totp_generatore:
    def __init__(self,key,uri,username,email):
        self.key = pyotp.random_base32()
        self.uri = pyotp.totp.TOTP(key).provisioning_uri(name=username, issuer_name=email)

    def generate_qrcode(self):
        return qrcode.make(self.uri)

        # metodo di verifica del totp
    def verify_totp(self,codice) -> bool:
        return pyotp.TOTP(self.key).verify(codice)





#se il return è vero allora
#return render_template('index.html')

#se è falso
#return render_template('login.html')
#prova pull