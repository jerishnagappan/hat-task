from flask import Blueprint

prompt_blueprint = Blueprint('prompt', __name__)

from yourproject.app.blueprints.project import routes