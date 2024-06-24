from your_project.app import db
from sqlalchemy.orm import validates
import datetime
import json
  

class Patent(db.Model):
    __tablename__ = 'patents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    application_number = db.Column(db.String(255), unique=True, nullable=False)
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
    patnum = db.Column(db.String(100), unique=True, nullable=False)
    abstract = db.Column(db.String(550), nullable=False)  


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'application_number': self.application_number,
            'inventor_name': self.inventor_name,
            'assignee_name_orig': self.assignee_name_orig,
            'assignee_name_current': self.assignee_name_current,
            'pub_date': self.convert_date(self.pub_date),
            'filing_date': self.convert_date(self.filing_date),
            'priority_date': self.convert_date(self.priority_date),
            'grant_date': self.convert_date(self.grant_date),
            'forward_cites_no_family': self.forward_cites_no_family,
            'forward_cites_yes_family': self.forward_cites_yes_family,
            'backward_cites_no_family': self.backward_cites_no_family,
            'backward_cites_yes_family': self.backward_cites_yes_family,
            'patnum': self.patnum,
            'abstract':self.abstract
        }

    def convert_date(self, date_value):
        if isinstance(date_value, str):
            
            try:
                return datetime.datetime.strptime(date_value, '%Y-%m-%d').date().isoformat()
            except ValueError:
                return None
        elif isinstance(date_value, datetime.date):
           
            return date_value.isoformat() if date_value else None
        else:
            return None



    
    @classmethod
    def delete_by_patnum_and_title(cls, patnum, title):
        patent = cls.query.filter_by(patnum=patnum, title=title).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def delete_by_patnum(cls, patnum):
        patent = cls.query.filter_by(patnum=patnum).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def delete_by_title(cls, title):
        patents = cls.query.filter_by(title=title).all()
        if patents:
            for patent in patents:
                db.session.delete(patent)
            db.session.commit()
            return True
        else:
            return False




    @classmethod
    def update_patent(cls, id, data):
        if not id:
            return False  
        patent = cls.query.get(id)
        if patent:
            for key, value in data.items():
                setattr(patent, key, value)
            db.session.commit()
            return True
        return False
    




    @classmethod
    def delete_inventor_name(cls, patnum, inventor_name):
        patent = cls.query.filter_by(patnum=patnum).first()
        if patent:
            inventor_names = json.loads(patent.inventor_name)
            new_inventor_names = [name for name in inventor_names if name['inventor_name'] != inventor_name]
            patent.inventor_name = json.dumps(new_inventor_names)
            db.session.commit()
            return True
        else:
            return False
        

    @classmethod
    def delete_patent(cls, patnum):
        patent = cls.query.filter_by(patnum=patnum).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return True
        return False

    @classmethod
    def delete_by_title(cls, title):
        patents = cls.query.filter_by(title=title).all()
        if patents:
            for patent in patents:
                db.session.delete(patent)
            db.session.commit()
            return True
        return False

    @classmethod
    def delete_by_application_number(cls, application_number):
        patents = cls.query.filter_by(application_number=application_number).all()
        if patents:
            for patent in patents:
                db.session.delete(patent)
            db.session.commit()
            return True
        return False

    @classmethod
    def delete_by_inventor_name(cls, inventor_name):
        patents = cls.query.filter_by(inventor_name=inventor_name).all()
        if patents:
            for patent in patents:
                db.session.delete(patent)
            db.session.commit()
            return True
        return False    












    












    # @classmethod
    # def get_patent_by_patnum(cls, patnum):
    #     return cls.query.filter_by(patnum=patnum).first()

    # def is_updated(self, new_data):
    #     return (self.title != new_data.get('title') or
    #             self.inventor_name != new_data.get('inventor_name') or
    #             self.assignee_name_orig != new_data.get('assignee_name_orig') or
    #             self.assignee_name_current != new_data.get('assignee_name_current') or
    #             self.pub_date != new_data.get('pub_date') or
    #             self.filing_date != new_data.get('filing_date') or
    #             self.priority_date != new_data.get('priority_date') or
    #             self.grant_date != new_data.get('grant_date') or
    #             self.forward_cites_no_family != new_data.get('forward_cites_no_family') or
    #             self.forward_cites_yes_family != new_data.get('forward_cites_yes_family') or
    #             self.backward_cites_no_family != new_data.get('backward_cites_no_family') or
    #             self.backward_cites_yes_family != new_data.get('backward_cites_yes_family'))

    # def update(self, data):
    #     self.title = data.get('title')
    #     self.inventor_name = data.get('inventor_name')
    #     self.assignee_name_orig = data.get('assignee_name_orig')
    #     self.assignee_name_current = data.get('assignee_name_current')
    #     self.pub_date = datetime.strptime(data.get('pub_date'), '%Y-%m-%d') if data.get('pub_date') else None
    #     self.filing_date = datetime.strptime(data.get('filing_date'), '%Y-%m-%d') if data.get('filing_date') else None
    #     self.priority_date = datetime.strptime(data.get('priority_date'), '%Y-%m-%d') if data.get('priority_date') else None
    #     self.grant_date = datetime.strptime(data.get('grant_date'), '%Y-%m-%d') if data.get('grant_date') else None
    #     self.forward_cites_no_family = data.get('forward_cites_no_family')
    #     self.forward_cites_yes_family = data.get('forward_cites_yes_family')
    #     self.backward_cites_no_family = data.get('backward_cites_no_family')
    #     self.backward_cites_yes_family = data.get('backward_cites_yes_family')
    #     db.session.commit()

#     def to_dict(self):
#     # Convert instance attributes to dictionary
#         return {
#             'id': self.id,
#             'title': self.title,
#             'application_number': self.application_number,
#             'inventor_name': self.inventor_name,
#             'assignee_name_orig': self.assignee_name_orig,
#             'assignee_name_current': self.assignee_name_current,
#             'pub_date': self.convert_date(self.pub_date),
#             'filing_date': self.convert_date(self.filing_date),
#             'priority_date': self.convert_date(self.priority_date),
#             'grant_date': self.convert_date(self.grant_date),
#             'forward_cites_no_family': self.forward_cites_no_family,
#             'forward_cites_yes_family': self.forward_cites_yes_family,
#             'backward_cites_no_family': self.backward_cites_no_family,
#             'backward_cites_yes_family': self.backward_cites_yes_family,
#             'patnum': self.patnum
#         }

# def convert_date(self, date_str):
#     # Helper function to convert date string to formatted date or None
#     if date_str:
#         try:
#             return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
#         except ValueError:
#             return None
#     return None


    # def to_dict(self):
    #     # Convert instance attributes to dictionary
    #     return {
    #         'id': self.id,
    #         'inventor_name': self.inventor_name,
    #         'assignee_name_orig': self.assignee_name_orig,
    #         'assignee_name_current': self.assignee_name_current,
    #         'pub_date': self.format_date(self.pub_date),
    #         'filing_date': self.format_date(self.filing_date),
    #         'priority_date': self.format_date(self.priority_date),
    #         'grant_date': self.format_date(self.grant_date),
    #         'forward_cites_no_family': self.forward_cites_no_family,
    #         'forward_cites_yes_family': self.forward_cites_yes_family,
    #         'backward_cites_no_family': self.backward_cites_no_family,
    #         'backward_cites_yes_family': self.backward_cites_yes_family,
    #         'patnum': self.patnum
    #     }

    # def format_date(self, date):
    #     # Helper function to format date or return None if date is None
    #     if date:
    #         return date.strftime('%Y-%m-%d')
    #     return None 












    # @classmethod
    # def insert_or_update(cls, data):
    #     patnum = data.get('patnum')
    #     existing_patent = cls.query.filter_by(patnum=patnum).first()

    #     if existing_patent:
    #         existing_patent.update(data)
    #     else:
    #         new_patent = cls(**data)
    #         db.session.add(new_patent)
    #     db.session.commit()

    # @classmethod
    # def get_patents(cls, patnums):
    #     return cls.query.filter(cls.patnum.in_(patnums)).all()








    # class Patent(db.Model):
#     __tablename__ = 'patents'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     application_number = db.Column(db.String(255), unique=True, nullable=False)
#     inventor_name = db.Column(db.JSON)
#     assignee_name_orig = db.Column(db.JSON)
#     assignee_name_current = db.Column(db.JSON)
#     pub_date = db.Column(db.Date)
#     filing_date = db.Column(db.Date)
#     priority_date = db.Column(db.Date)
#     grant_date = db.Column(db.Date)
#     forward_cites_no_family = db.Column(db.JSON)
#     forward_cites_yes_family = db.Column(db.JSON)
#     backward_cites_no_family = db.Column(db.JSON)
#     backward_cites_yes_family = db.Column(db.JSON)
#     patnum = db.Column(db.String(100), unique=True, nullable=False)
#     abstract = db.column(db.String(1250),nullable = False)