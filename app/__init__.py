import os
import json

from dotenv import load_dotenv, find_dotenv

from flask import Flask, Blueprint, g

from flask_restful import Api, Resource
from flask_cors import CORS

from pymongo import MongoClient
from utils.json_encoder import CustomJSONEncoder
from app.blueprints.website import website_bp
from app.blueprints.zinny import zinny_bp



app = Flask(__name__)
cors = CORS(app)

load_dotenv(find_dotenv())
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.json_encoder = CustomJSONEncoder

@app.teardown_appcontext
def close_mongo_connection(exception):
    mongo_client = g.pop('mongo_client', None) # Get the client from 'g'
    if mongo_client is not None:
        mongo_client.close() # Close it if it exists

app.register_blueprint(website_bp)
app.register_blueprint(zinny_bp)

