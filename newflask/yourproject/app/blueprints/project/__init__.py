from flask import Blueprint

project_blueprint = Blueprint('project', __name__)

from yourproject.app.blueprints.project import routes

