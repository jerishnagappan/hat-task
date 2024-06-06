import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Prompt(db.Model):
    __tablename__ = 'prompts'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    @staticmethod
    def create(name, project_id):
        new_prompt = Prompt(name=name, project_id=project_id)
        db.session.add(new_prompt)
        db.session.commit()
    
    @staticmethod
    def update(prompt_id, new_name):
        prompt = Prompt.query.get(prompt_id)
        if prompt:
            prompt.name = new_name
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def delete(prompt_id):
        prompt = Prompt.query.get(prompt_id)
        if prompt:
            db.session.delete(prompt)
            db.session.commit()
            return True
        return False

def insert_to_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            project = Project.query.filter_by(name=app).first()
            if project:
                new_prompt = Prompt(name=app, project_id=project.id)
                db.session.add(new_prompt)
        db.session.commit()
        return True
    
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
        db.session.rollback()
        return False


def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df 


if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        success = insert_to_the_table(df)
        if success:
            print("Data inserted successfully.")
        else:
            print("Failed to insert data.")






# # Example usage 
# create("Alice")
# add_product("Sample Product")

# for user in users:
#     print(user.id, user.name, user.age)
# update_user(1, "Haley", 25)
# delete_user(1)