from yourproject.app.extensions import db
from yourproject.app.schemas import PromptSchema
from marshmallow.exceptions import ValidationError




# class Project(db.Model):
#     __tablename__ = 'projects'
#     __table_args__ = {'schema': 'jerish'}
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True, nullable=False)

    # @staticmethod
    # def create(name):
    #     new_project = Project(name=name)
    #     db.session.add(new_project)
    #     db.session.commit()
        
    #     return new_project

    # @staticmethod
    # def update(project_id, new_name):
    #     project = Project.query.get(project_id)
    #     if project:
    #         project.name = new_name
    #         db.session.commit()
            
    #         return project
    #     return None

    # @staticmethod
    # def delete(project_id):
    #     project = Project.query.get(project_id)
    #     if project:
    #         db.session.delete(project)
    #         db.session.commit()
            
    #         return project
    #     return None
    



class Prompt(db.Model):
    __tablename__ = 'prompts'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)





    @classmethod
    def add(cls, project_id, name):
        new_prompt = cls(project_id=project_id, name=name)
        db.session.add(new_prompt)
        db.session.commit()
        return new_prompt

    @classmethod
    def get(cls, prompt_id):
        return cls.query.get(prompt_id)

    def update(self, name):
        self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#     @classmethod
#     def create(cls, name, project_id):
#         new_prompt = cls(name=name, project_id=project_id)
#         db.session.add(new_prompt)
#         db.session.commit()
#         return new_prompt
    
#     @classmethod
#     def update(cls, prompt_id, new_name):
#         prompt = cls.query.get(prompt_id)
#         if prompt:
#             prompt.name = new_name
#             db.session.commit()
            
#             return prompt
#         return None
    
#     @classmethod
#     def delete(cls, prompt_id):
#         prompt = cls.query.get(prompt_id)
#         if prompt:
#             db.session.delete(prompt)
#             db.session.commit()
#             return True
#         return False



# class Version(db.Model):
#     __tablename__ = 'versions'
#     __table_args__ = {'schema': 'jerish'}
#     id = db.Column(db.Integer, primary_key=True)
#     prompt_id = db.Column(db.Integer, db.ForeignKey('jerish.prompts.id'), nullable=True)
#     prompt_text = db.Column(db.String(255), nullable=False)


#     @staticmethod
#     def create(prompt_id, prompt_text):
#         new_version = Version(prompt_id=prompt_id, prompt_text=prompt_text)
#         db.session.add(new_version)
#         db.session.commit()
        
#         return new_version
    
#     @staticmethod
#     def update(version_id, new_prompt_text):
#         version = Version.query.get(version_id)
#         if version:
#             version.prompt_text = new_prompt_text
#             db.session.commit()
            
#             return version  
#         return None
    
#     @staticmethod
    # def delete(version_id):
    #     version = Version.query.get(version_id)
    #     if version:
    #         db.session.delete(version)
    #         db.session.commit()
            
    #         return version  
    #     return None






