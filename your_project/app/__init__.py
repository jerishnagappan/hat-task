

from fla import Flask
from flask_sqlalchemy import SQLAlchemy
from your_project.app.extensions import db
from your_project.app.models.patent import Patent
from your_project.app.schemas import PatentSchema
from your_project.app.blueprints.patent.routes import update_patent_details


# db = SQLAlchemy()
# patent_schema = PatentSchema()

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)


    db.init_app(app)

    
    from your_project.app.blueprints.patent.routes import patents_bp
    app.register_blueprint(patents_bp, url_prefix='/patents')


    return app
