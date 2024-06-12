from yourproject.app.extensions import db





# class Prompt(db.Model):
#     __tablename__ = 'prompts'
#     __table_args__ = {'schema': 'jerish'}
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
#     name = db.Column(db.String(255), nullable=False)



class Version(db.Model):
    __tablename__ = 'versions'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey('jerish.prompts.id'), nullable=True)
    prompt_text = db.Column(db.String(255), nullable=False)





    @classmethod
    def add(cls, prompt_id, prompt_text):
        new_version = cls(prompt_id=prompt_id, prompt_text=prompt_text)
        db.session.add(new_version)
        db.session.commit()
        return new_version

    @classmethod
    def get(cls, version_id):
        return cls.query.get(version_id)

    def update(self, prompt_text):
        self.prompt_text = prompt_text
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

