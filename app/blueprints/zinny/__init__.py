# blueprints/users/__init__.py
from flask import Blueprint
from flask_restful import Api
from app.blueprints.zinny.zinny import ZinnyDataLatest, ZinnyDataList, ZinnyCalibrationLatest



# Create the Blueprint
zinny_bp = Blueprint('zinny_api', __name__, url_prefix='/api/v1/zinny')

# Create a Flask-RESTful API instance attached to this Blueprint
api = Api(zinny_bp)


api.add_resource(ZinnyDataLatest, "/zinny-data/latest")
api.add_resource(ZinnyDataList, "/zinny-data")
api.add_resource(ZinnyCalibrationLatest, "/zinny-calibration/latest")