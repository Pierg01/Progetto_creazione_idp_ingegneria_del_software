import pyotp
import qrcode

secret_key = "Pippo"  # Generate a random secret key
uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name="Rocco",
                                                   issuer_name="Roc")

qrcode.make(uri).save("qrcode.png")

#metodo di verifica del totp
def verify_totp(token):
    return pyotp.TOTP(secret_key).verify(token)


#se il return è vero allora
#return render_template('index.html')

#se è falso
#return render_template('login.html')


