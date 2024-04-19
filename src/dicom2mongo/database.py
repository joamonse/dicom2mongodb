import pymongo
from typing import List

class Database:
    def __init__(self, url: str, port: int, db_name: str):
        self.client = pymongo.MongoClient(url, port)
        self.db = self.client[db_name]


    def insert(self, data: dict, collection_name: str) -> None:
        collection = self.db[collection_name]
        collection.insert_one(data)


    def get_tags_list(self, collection_name: str) -> List[dict]:
        collection = self.db[collection_name]
        return collection.find()
