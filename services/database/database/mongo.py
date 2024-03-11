import uuid

from pymongo import MongoClient

from .config import DatabaseConfig

config = DatabaseConfig()


class MongoRepository:
    def __init__(self, collection: str):
        self.client = MongoClient(str(config.mongo_dns), uuidRepresentation="standard")
        database_name = config.mongo_dns.path.replace("/", "", 1)  # type: ignore
        self.db = self.client[database_name]
        self.collection = self.db[collection]

    def insert(self, data: dict):
        self.collection.insert_one(data)

    def find(self, query: dict):
        result = self.collection.find(query)
        if result:
            result = list(result)
            for i in range(len(result)):
                result[i].pop("_id")
        else:
            result = []
        return result

    def find_one(self, query: dict):
        result = self.collection.find_one(query)
        if result:
            result.pop("_id")
        return result

    def update(self, query: dict, data: dict):
        self.collection.update_one(query, {"$set": data})

    def delete(self, query: dict):
        self.collection.delete_one(query)
