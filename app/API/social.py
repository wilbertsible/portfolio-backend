from flask import Blueprint
from flask_restful import Resource
from app import new_connection
import json

class Social(Resource):
    social = Blueprint("Social",__name__)
    def get(self):
        cursor  = new_connection.db["social"].find({},{"_id":0, "name":1,"icon":1,"link":1, "is_active":1}).sort("name",1)
        list_cur = list(cursor)
        json_data = json.dumps(list_cur)
        return json_data