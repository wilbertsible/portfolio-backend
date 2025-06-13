import os
import json

from dotenv import load_dotenv, find_dotenv

from flask import Flask, Blueprint

from flask_restful import Api, Resource
from flask_cors import CORS

from pymongo import MongoClient
from utils.json_encoder import CustomJSONEncoder
from app.blueprints.website import website_bp
from app.blueprints.zinny import zinny_bp


app = Flask(__name__)            
cors = CORS(app)

load_dotenv(find_dotenv())
user = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASS')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.mongo_client = MongoClient(app.config["MONGO_URI"])
app.json_encoder = CustomJSONEncoder

app.register_blueprint(website_bp)
app.register_blueprint(zinny_bp)

