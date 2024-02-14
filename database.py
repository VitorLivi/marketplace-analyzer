from pymongo import MongoClient

class Database:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
            cls.__instance = cls.connect_to_database()
        return cls.__instance

    def connect_to_database():
       CONNECTION_STRING = "mongodb+srv://root:123@localhost:27017/analytics"
       client = MongoClient(CONNECTION_STRING)
       return client

