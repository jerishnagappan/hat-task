from flask import Blueprint

version_blueprint = Blueprint('version', __name__)

from yourproject.app.blueprints.project import routes