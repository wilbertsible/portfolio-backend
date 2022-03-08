from flask import Blueprint
from flask_restful import Resource
from app import new_connection
import json

class Header(Resource):
    header = Blueprint("Header",__name__)
    def get(self):
        cursor  = new_connection.db["header_section"].find({},{"_id":0, "title":1,"link":1,"is_active":1}).sort("headerId",1)
        list_cur = list(cursor)
        json_data = json.dumps(list_cur)
        return json_data