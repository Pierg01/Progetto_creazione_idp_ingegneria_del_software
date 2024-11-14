import pymongo


def search_user(utente: dict) -> dict:
    dbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbs.get_database("Idp_User")
    collection = db.get_collection("Idp_User")
    users=collection.find_one().get("Utenti")
    if users:
        for user in users:
            if user.get("Username")==utente.get("Username"):
                return user
    return {"Username":None,"Password":None}




def compare_password(password1, password2) -> bool:
    return password1 == password2
