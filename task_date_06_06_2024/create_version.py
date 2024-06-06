import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)



class Prompt(db.Model):
    __tablename__ = 'prompts'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


class Version(db.Model):
    __tablename__ = 'versions'
    __table_args__ = {'schema' : 'jerish'}

    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey('jerish.prompts.id'), nullable=True)
    prompt_text = db.Column(db.String(555), nullable=False)

    @staticmethod
    def create(prompt_id, prompt_text):
        new_version = Version(prompt_id=prompt_id, prompt_text=prompt_text)
        db.session.add(new_version)
        db.session.commit()
    
    @staticmethod
    def update(version_id, new_prompt_text):
        version = Version.query.get(version_id)
        if version:
            version.prompt_text = new_prompt_text
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def delete(version_id):
        version = Version.query.get(version_id)
        if version:
            db.session.delete(version)
            db.session.commit()
            return True
        return False



def insert_to_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            prompt_text = row['Prompt']
            existing_project = Prompt.query.filter_by(name=app).first()
            
            if existing_project:
                prompt = Prompt.query.filter_by(name=app).first()
                
                if prompt:
                    Version.create(prompt_id=prompt.id, prompt_text=prompt_text)
                else:
                    print(f"Prompt for project '{app}' not found in the database.")
            else:
                print(f"Project '{app}' not found in the database.")
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