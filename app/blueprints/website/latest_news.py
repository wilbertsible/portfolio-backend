from flask_restful import Resource
from flask import request, jsonify, current_app
from app.db_helpers import get_mongo_db

class LatestNews(Resource):

    def get(self):
        db = get_mongo_db("websitedb")
        query = {}
        projection={
            "_id": 0,          # Exclude MongoDB's default _id field
            "date_added": 1,
            "latest_news": 1,
        }
        sort = [('_id', -1)]
        latest_news_data = db["latest_news"].find_one(query, projection, sort=sort)
        if latest_news_data:
            return jsonify(latest_news_data)
        else:
            return jsonify({"error": "Latest News not found"}), 404