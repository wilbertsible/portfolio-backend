from flask_restful import Resource
from flask import request, jsonify, current_app

class Social(Resource):

    def get(self):
        db = current_app.mongo_client.websitedb
        query = {}
        projection={
            "_id": 0,          # Exclude MongoDB's default _id field
            "name": 1,
            "icon": 1,
            "link": 1,
            "is_active": 1
        }
        socials_list = list(db["social"].find(query,projection))
        if socials_list:
            return jsonify(socials_list)
        else:
            return jsonify({"error": "Socials List not found"}), 404