import pyotp

secret_key = pyotp.random_base32()  # Generate a random secret key

#Generazione del codice TOTP
def generate_TOTP(secret_key):
    totp = pyotp.TOTP(secret_key)

#Verifica del codice TOTP
def verify_TOTP(totp):
    pyotp.verify(totp)

#Totp via mail

