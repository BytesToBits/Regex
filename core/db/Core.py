from pymongo import MongoClient
from core.enums import Bot

client = MongoClient(Bot.MONGO_URI)

class BaseDB:
    def __init__(self, db="main", col=""):
        self.db = client[db]
        self.col = self.db[col]