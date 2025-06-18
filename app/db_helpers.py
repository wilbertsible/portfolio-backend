# app/db_helpers.py
from flask import g, current_app
from pymongo import MongoClient

def get_mongo_client():
    """
    Gets a MongoClient instance for the current request/worker.
    Initializes it if it doesn't already exist in the 'g' object.
    """
    if 'mongo_client' not in g:
        g.mongo_client = MongoClient(current_app.config["MONGO_URI"])
    return g.mongo_client

def get_mongo_db(db_name="zinny"): # Set default to "zinny" if that's your primary DB
    """
    Gets a specific MongoDB database instance from the client.
    """
    client = get_mongo_client()
    # You could also cache the db instance in g if you access multiple dbs frequently
    # if 'mongo_db' not in g or g.mongo_db.name != db_name:
    #     g.mongo_db = client.get_database(db_name)
    # return g.mongo_db
    return client.get_database(db_name) # Simpler, always gets it from client