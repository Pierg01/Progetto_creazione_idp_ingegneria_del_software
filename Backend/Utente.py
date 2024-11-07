import pymongo
import pprint





class Utente:

    def __init__(self,name: str,password: str):
        self.name=name
        self.password=password

    def search(self,utente: dict):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        collection = client["Idp_User"]
        if collection.find_one({"name":utente["name"]}) is None:
            return {"name": None, "password": None}
        else:
            user = collection.find_one({"name":utente["name"]})
            self.name = user["name"]
            self.password = user["password"]


    def compare_password(self,password) -> bool:
        return  password == self.password






