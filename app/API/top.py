from flask import Blueprint
from flask_restful import Resource
from app import new_connection
import json

class Top(Resource):
    header = Blueprint("Header",__name__)
    def get(self):
        return('',204)