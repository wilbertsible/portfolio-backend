from flask import Blueprint
from flask_restful import Resource
from app import new_connection
import json

class ProjectsList(Resource):
    def get(self):
        cursor  = new_connection.db["content"].find({},{"_id":0, "title":1,"bannerImage":1,"fileName":1,"is_active":1,"tags":1,"dateUploaded":1}).sort("contentId",-1)
        list_cur = list(cursor)
        json_data = json.dumps(list_cur,default=str)
        return json_data