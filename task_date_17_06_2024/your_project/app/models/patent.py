from your_project.app.extensions import db
from your_project.app.schemas import PatentSchema
from marshmallow.exceptions import ValidationError

class Patent(db.Model):
    __tablename__ = 'patent'
    __table_args__ = {'schema': 'jerish', 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    application_number = db.Column(db.String(50), unique=True)
    inventor_name = db.Column(db.String(100))
    assignee_name_orig = db.Column(db.String(200))
    assignee_name_current = db.Column(db.String(200))
    pub_date = db.Column(db.Date)
    filing_date = db.Column(db.Date)
    priority_date = db.Column(db.Date)
    grant_date = db.Column(db.Date)
    forward_cites_no_family = db.Column(db.Integer)
    forward_cites_yes_family = db.Column(db.Integer)
    backward_cites_no_family = db.Column(db.Integer)
    backward_cites_yes_family = db.Column(db.Integer)

    @classmethod
    def get_details(cls, patnums):
        patents = cls.query.filter(cls.application_number.in_(patnums)).all()
        return patents

    @classmethod
    def delete_details(cls, patnum):
        patent = cls.query.filter_by(application_number=patnum).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return True
        return False

    @classmethod
    def update_details(cls, patnum, data):
        patent = cls.query.filter_by(application_number=patnum).first()
        if patent:
            try:
                schema = PatentSchema()
                validated_data = schema.load(data)
                for key, value in validated_data.items():
                    if getattr(patent, key) != value:
                        setattr(patent, key, value)
                db.session.commit()
                return True
            except ValidationError as err:
                db.session.rollback()
                raise err
        return False
