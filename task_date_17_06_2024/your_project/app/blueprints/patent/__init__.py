from flask import Blueprint

patent_blueprint = Blueprint('patent', __name__)

from your_project.app.blueprints.patent import routes




