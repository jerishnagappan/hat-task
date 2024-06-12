from yourproject.app.extensions import db
from yourproject.app.schemas import ProjectSchema
from marshmallow.exceptions import ValidationError

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'jerish', 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    @classmethod
    def add(cls, data):
        try:
            project = ProjectSchema.load(data)
            db.session.add(project)
            db.session.commit()
            return project
        except ValidationError as err:
            db.session.rollback()
            raise err

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def update_by_id(cls, id, data):
        project = cls.query.get_or_404(id)
        try:
            project = ProjectSchema.load(data, instance=project, partial=True)
            db.session.commit()
            return project
        except ValidationError as err:
            db.session.rollback()
            raise err

    @classmethod
    def delete_by_id(cls, id):
        project = cls.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()








