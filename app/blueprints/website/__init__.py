# blueprints/users/__init__.py
from flask import Blueprint
from flask_restful import Api
from app.blueprints.website.project_resources import Project, ProjectsList
from app.blueprints.website.social import Social  


# Create the Blueprint
website_bp = Blueprint('website_api', __name__, url_prefix='/api/v1/website')

# Create a Flask-RESTful API instance attached to this Blueprint
api = Api(website_bp)


api.add_resource(Social, "/social")
api.add_resource(ProjectsList, "/projects")
api.add_resource(Project, "/projects/<string:projectName>")