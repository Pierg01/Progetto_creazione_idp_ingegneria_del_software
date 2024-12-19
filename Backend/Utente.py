import secrets

import pymongo


def search_user(utente: str) -> dict:
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db.get_collection("Idp_User")
    user = collection.find_one({"Utenti.Username": utente}, {"Utenti.$": 1})
    if user and "Utenti" in user:
        return user["Utenti"][0]
    return None


def search_user_email(email: str) -> dict:
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db.get_collection("Idp_User")
    user = collection.find_one({"Utenti.Email": email}, {"Utenti.$": 1})
    if user and "Utenti" in user:
        return user["Utenti"][0]
    return None


def get_key(utente: str) -> str:
    utente = search_user(utente)
    return utente["chiave segreta"]


def get_key_email(email: str) -> str:
    utente = search_user(email)
    print("SONO NEL METODO PER AVERE LA CHIAVE DALLA EMAIL")
    return utente["chiave segreta"]


def insert_user(user):
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db["Idp_User"]
    collection.update_one(
        {"Utenti": {"$exists": True}},
        {"$push": {"Utenti": user}}
    )


def compare_password(password1, password2) -> bool:
    return password1 == password2


def get_key_token(user: dict):
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db["Idp_User"]
    username = user["Username"]
    utente = search_user(username)
    if utente["Key token"] == "":
        key = secrets.token_hex(32)
        # utente["Key token"]=key
        collection.update_one(
            {"Utenti.Username": username},
            {"$set": {"Utenti.$.Key token": key}}
        )
        return key
    else:
        return utente["Key token"]

def cambio_psw(user: dict, new_psw: str):
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db["Idp_User"]
    username = user["Username"]
    collection.update_one(
        {"Utenti.Username": username},
        {"$set": {"Utenti.$.Password": new_psw}}
    )

