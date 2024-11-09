import jwt

def codifica(messaggio: dict,private_key: str) -> dict:
    messaggio_criptato = jwt.encode(messaggio,private_key,"HS256")
    return messaggio_criptato
