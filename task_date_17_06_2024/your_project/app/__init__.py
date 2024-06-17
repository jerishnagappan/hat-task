
from flask import Flask
from your_project.app.extensions import db
from your_project.app.blueprints.patent import patent_blueprint

from your_project.app.config import Config


def create_app():
    app = Flask(__name__)

    
    app.config.from_object(Config)

    
    db.init_app(app)

    
    app.register_blueprint(patent_blueprint, url_prefix='/patent')
    
    return app