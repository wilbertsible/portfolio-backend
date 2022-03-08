from pymongo import MongoClient

class MongoDatabase():
    
    def __init__(self, db, user, password):
        self.client = MongoClient(f"mongodb+srv://{user}:{password}@wilbertcluster.qizcp.mongodb.net/websitedb?retryWrites=true&w=majority")
        self.db = self.client[db]
