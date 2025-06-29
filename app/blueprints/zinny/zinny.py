from flask_restful import Resource
from flask import request, jsonify, current_app
from app.db_helpers import get_mongo_db


class ZinnyDataLatest(Resource):

    def get(self):
        db = get_mongo_db("zinny")
        query = {}
        projection={
            "_id": 0,
            "sunlight_level": 1,
            "temperature": 1,
            "humidity": 1,
            "soil_moisture": 1,
            "total_daily_dispensed_water": 1,
            "timestamp": 1,
        }
        sort = [('_id', -1)]
        zinny_latest = db["zinny_data"].find_one(query,projection, sort=sort)
        if zinny_latest:
            return jsonify(zinny_latest)
        else:
            return jsonify({"error": "Latest Zinny Data not found"}), 404



class ZinnyDataList(Resource):

    def get(self):
        db = get_mongo_db("zinny")
        query = {}
        projection={
            "_id": 0,          # Exclude MongoDB's default _id field
            "sunlight_level": 1,
            "temperature": 1,
            "humidity": 1,
            "soil_moisture": 1,
            "total_daily_dispensed_water": 1,
            "timestamp": 1,
        }
        sort = [('_id', -1)]
        zinny_all = list(db["zinny_data"].find(query, projection, sort=sort))
        if zinny_all:
            return jsonify(zinny_all)
        else:
            return jsonify({"error": "Zinny Data not found"}), 404


class ZinnyCalibrationLatest(Resource):

    def get(self):
        db = get_mongo_db("zinny")
        query = {}
        projection={
            "_id": 0,
            "date": 1,
            "slope": 1,
            "y_intercept": 1,
        }
        sort = [('_id', -1)]
        zinny_calibration_latest = db["zinny_calibration"].find_one(query,projection, sort=sort)
        if zinny_calibration_latest:
            return jsonify(zinny_calibration_latest)
        else:
            return jsonify({"error": "Latest Zinny Calibration Data not found"}), 404


class ZinnyDataAggregate(Resource):
    def get(self, start_date, end_date):
        db = get_mongo_db("zinny")
        query = {
            'timestamp':{
                '$gte':start_date,
                '$lte':end_date
            }
        }
        projection={
            "_id": 0,          # Exclude MongoDB's default _id field
            "sunlight_level": 1,
            "temperature": 1,
            "humidity": 1,
            "soil_moisture": 1,
            "total_daily_dispensed_water": 1,
            "timestamp": 1,
        }
        zinny_all = list(db["zinny_data"].find(query, projection))
        if zinny_all:
            return jsonify(zinny_all)
        else:
            return jsonify({"error": "Zinny Data not found"}), 404