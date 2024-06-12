from flask import Flask
from yourproject.app.extensions import db
from yourproject.app.blueprints.project import project_blueprint
from yourproject.app.blueprints.prompt import prompt_blueprint
from yourproject.app.blueprints.version import version_blueprint
from yourproject.app.config import Config


def create_app():
    app = Flask(__name__)

    
    app.config.from_object(Config)

    
    db.init_app(app)

    
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(prompt_blueprint, url_prefix='/prompt')
    app.register_blueprint(version_blueprint, url_prefix='/version')

    return app
