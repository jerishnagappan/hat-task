from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Patent(db.Model):
    __tablename__ = 'patents'

    id = db.Column(db.Integer, primary_key=True)
    patnum = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255))
    application_number = db.Column(db.String(50))
    inventor_name = db.Column(db.JSON)
    assignee_name_orig = db.Column(db.JSON)
    assignee_name_current = db.Column(db.JSON)
    pub_date = db.Column(db.Date)
    filing_date = db.Column(db.Date)
    priority_date = db.Column(db.Date)
    grant_date = db.Column(db.Date)
    forward_cites_no_family = db.Column(db.JSON)
    forward_cites_yes_family = db.Column(db.JSON)
    backward_cites_no_family = db.Column(db.JSON)
    backward_cites_yes_family = db.Column(db.JSON)
    abstract = db.Column(db.String(1250), nullable=False)  # Adjust max length as needed


    def __repr__(self):
        return f'<Patent {self.patnum}>'
