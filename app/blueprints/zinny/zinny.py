from flask_restful import Resource
from flask import request, jsonify, current_app
from app.db_helpers import get_mongo_db
from datetime import datetime, timedelta


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
        return jsonify(zinny_all)


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
    def get(self, duration):
        db = get_mongo_db("zinny")
        datetime_now = datetime.now()
        start_time = None
        pipeline = None
        if duration == 'hour':
            start_time = datetime_now - timedelta(hours=1)
            pipeline = [
                {
                    '$match':{
                        "timestamp":{
                            "$gte":start_time,
                            "$lte":datetime_now
                        }
                    }
                },
                {
                    '$project': {
                        "_id": 0,          # Exclude MongoDB's default _id field
                        "sunlight_level": 1,
                        "temperature": 1,
                        "humidity": 1,
                        "soil_moisture": 1,
                        "total_daily_dispensed_water": 1,
                        "timestamp": 1,
                    }
                },
                {
                    '$sort': {
                        'timestamp': 1
                    }
                }
            ]
        elif duration == '12-hour':
            start_time = datetime_now - timedelta(hours=12)
            pipeline = [
                {
                    '$match': {
                        'timestamp': {
                            '$gte': start_time,
                            '$lte': datetime_now
                        }
                    }
                },
                {
                    '$sort': {
                        'timestamp': 1 
                    }
                },
                {
                    '$group': {
                        '_id': {
                            '$dateTrunc': {
                                'date': '$timestamp',
                                'unit': 'minute',
                                'binSize': 20,
                            }
                        },
                        'actual_timestamp_in_bin': {'$first': '$timestamp'},
                        'sunlight_level': { '$first': "$sunlight_level" },
                        'humidity_temperature': { '$first': "$humidity" },
                        'temperature':{'$first':'$temperature'},
                        'soil_moisture': { '$first': "$soil_moisture" }
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'actual_timestamp_in_bin': 1,
                        "sunlight_level": 1,
                        "temperature": 1,
                        "humidity": 1,
                        "soil_moisture": 1,
                        "total_daily_dispensed_water": 1,
                        "timestamp": 1,
                    }
                },
                {
                    '$sort': {
                        'actual_timestamp_in_bin': 1
                    }
                }
            ]
        elif duration == 'day':
            start_time = datetime_now - timedelta(days=1)
            pipeline = [
                {
                    '$match': {
                        'timestamp': {
                            '$gte': start_time,
                            '$lte': datetime_now
                        }
                    }
                },
                {
                    '$sort': {
                        'timestamp': 1
                    }
                },
                {
                    '$group': {
                        '_id': {
                            '$dateTrunc': {
                                'date': '$timestamp',
                                'unit': 'hour',
                                'binSize': 1,
                            }
                        },
                        'actual_timestamp_in_bin': {'$first': '$timestamp'},
                        'sunlight_level': { '$first': "$sunlight_level" },
                        'humidity_temperature': { '$first': "$humidity" },
                        'temperature':{'$first':'$temperature'},
                        'soil_moisture': { '$first': "$soil_moisture" }
                    
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'actual_timestamp_in_bin': 1,
                        "sunlight_level": 1,
                        "temperature": 1,
                        "humidity": 1,
                        "soil_moisture": 1,
                        "total_daily_dispensed_water": 1,
                        "timestamp": 1,
                    }
                },
                {
                    '$sort': {
                        'actual_timestamp_in_bin': 1
                    }
                }
            ]
        elif duration == 'week':
            start_time = datetime_now - timedelta(days=7)
            pipeline = [
                    {
                        '$match': {
                            'timestamp': {
                                '$gte': start_time,
                                '$lte': datetime_now
                            }
                        }
                    },
                    {
                        '$sort': {
                            'timestamp': 1
                        }
                    },
                    {
                        '$group': {
                            '_id': {
                                '$dateTrunc': {
                                    'date': '$timestamp',
                                    'unit': 'hour',
                                    'binSize': 6,
                                }
                            },
                            'documentCount': {'$sum': 1},
                            'avg_sunlight_level': {'$avg': '$sunlight_level'},
                            'avg_temperature': {'$avg': '$temperature'},
                            'avg_humidity': {'$avg': '$humidity'},
                            'avg_soil_moisture': {'$avg': '$soil_moisture'}
                        }
                    },
                    {
                        '$project': {
                            '_id': 0,
                            'timestamp': '$_id',
                            'documentCount': 1,
                            'avg_sunlight_level': 1,
                            'avg_temperature': 1,
                            'avg_humidity': 1,
                            'avg_soil_moisture': 1
                        }
                    },
                    {
                        '$sort': {
                            'timestamp': 1
                        }
                    }
                ]
        else:
            # Handle unknown duration or provide a default
            return jsonify({"error": "Invalid duration specified"}), 400
        
        zinny_aggregate = list(db["zinny_data"].aggregate(pipeline))
        print(zinny_aggregate)
        return jsonify(zinny_aggregate)