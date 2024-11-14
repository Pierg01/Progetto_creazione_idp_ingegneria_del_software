import pymongo


def search_user(utente: str) -> dict:
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db.get_collection("Idp_User")
    users=collection.find_one().get("Utenti")
    if users:
        for user in users:
            if user.get("Username")==utente:
                return user
    return {"Username":None,"Password":None}


def get_key(utente: str) -> str:
    utente = search_user(utente)
    return utente["chiave_segreta"]


def insert_user(user):
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db.get_collection("Idp_User")
    collection.get("Utenti")
    collection.



def compare_password(password1, password2) -> bool:
    return password1 == password2
