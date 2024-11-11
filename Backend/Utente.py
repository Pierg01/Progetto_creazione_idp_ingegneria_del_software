import pymongo


class Utente:

    def __init__(self,username: str,password: str):
        self.Username=username
        self.password=password


    def search(self,utente: dict) -> dict:
        client = pymongo.MongoClient("/mongodb+srv://pligorii1:<Mongodb01>@cluster0.rhvxckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        collection = client["Idp_user"]

        if collection.Utenti.find({"Username":utente["username"]}) is None:
            return {"Username": None, "password": None}
        else:
            users = collection.Utenti.find({"Username": utente["username"]})
            for user in users:
                self.Username=user["Username"]
                self.password=user["password"]

    def compare_password(self,password) -> bool:
        return  password == self.password





