from re import search

import pymongo
import pprint





class Utente:

    def __init__(self,name: str,password: str):
        self.name=name
        self.password=password

    def search(self,utente: dict):
        client = pymongo.MongoClient("mongodb+srv://pligorii1:<Mongodb01>@cluster0.rhvxckx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        collection = client["Idp_user"]
        print(client)
        if collection.find_one({"name":utente["name"]}) is None:
            return {"name": None, "password": None}
        else:
            user = collection.find_one({"name":utente["name"]})
            self.name = user["name"]
            self.password = user["password"]


    def compare_password(self,password) -> bool:
        return  password == self.password


if __name__ == "__main__":
    Utente.search({"name":"coglioone","password":"checco"})
