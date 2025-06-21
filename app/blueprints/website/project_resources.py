from flask_restful import Resource
from flask import request, jsonify, current_app
from app.db_helpers import get_mongo_db

class Project(Resource):

    def get(self,projectName):
        db = get_mongo_db("websitedb")
        query = {'url': projectName}
        projection={
            "_id": 0,          # Exclude MongoDB's default _id field
            "title": 1,
            "bannerImage": 1,
            "fileName": 1,
            "is_active": 1,
            "body": 1,
            "url": 1,
            "tags": 1,
        }
        project_data = db["content"].find_one(query,projection)
        if project_data:
            return jsonify(project_data)
        else:
            return jsonify({"error": "Project not found"}), 404

class ProjectsList(Resource):

    def get(self):
        db = get_mongo_db("websitedb")
        query = {}
        projection = {
            "_id": 0,          # Exclude MongoDB's default _id field
            "title": 1,
            "bannerImage": 1,
            "fileName": 1,
            "is_active": 1,
            "tags": 1,
            "dateUploaded": 1,
            "url": 1
        }
        sort = [('_id', -1)]
        projects_list = list(db["content"].find(query,projection, sort=sort))
        if projects_list:
            return jsonify(projects_list)
        else:
            return jsonify({"error": "List not found"}), 404