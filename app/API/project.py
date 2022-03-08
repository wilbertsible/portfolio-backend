from flask import Blueprint
from flask_restful import Resource
from app import new_connection
import json

class Project(Resource):
    def get(self,projectName):
        query = {}
        query['fileName'] = projectName
        cursor  = new_connection.db["content"].find(query,{"_id":0, "title":1,"bannerImage":1,"fileName":1,"is_active":1,"body":1}).sort("contentId",1)
        list_cur = list(cursor)
        json_data = json.dumps(list_cur)
        return json_data