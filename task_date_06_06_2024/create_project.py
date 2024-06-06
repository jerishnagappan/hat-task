import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
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
    
    @staticmethod
    def create(name):
        new_project = Project(name=name)
        db.session.add(new_project)
        db.session.commit()
    
    @staticmethod
    def update(project_id, new_name):
        project = Project.query.get(project_id)
        if project:
            project.name = new_name
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def delete(project_id):
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return True
        return False

def insert_to_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            existing_project = Project.query.filter_by(name=app).first()
            if not existing_project:
                Project.create(app)
        return True
    except IntegrityError:
        db.session.rollback()
        return False
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






