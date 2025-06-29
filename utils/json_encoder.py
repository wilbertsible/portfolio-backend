import json
from datetime import datetime
from bson import ObjectId # Assuming you're using pymongo
from bson.timestamp import Timestamp # Import Timestamp

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat() # Convert datetime to ISO format

        if isinstance(obj, Timestamp):

            return obj.as_datetime().isoformat()
        return json.JSONEncoder.default(self, obj)
        