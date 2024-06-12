from yourproject.app.extensions import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
