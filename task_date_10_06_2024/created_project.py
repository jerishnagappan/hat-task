import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import configparser
import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import logging


config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)


logging.basicConfig(filename='apps.log', level= logging.INFO)

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
        logging.info(f"Created project: {name}")
        return new_project

    @staticmethod
    def update(project_id, new_name):
        project = Project.query.get(project_id)
        if project:
            project.name = new_name
            db.session.commit()
            logging.info(f"Updated project with ID {project_id} to name: {new_name}")
            return project
        return None

    @staticmethod
    def delete(project_id):
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            logging.info(f"Deleted project with ID {project_id}")
            return project
        return None


    
def insert_into_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            existing_project = Project.query.filter_by(name=app).first()
            if not existing_project:
                Project.create(name=app)
        db.session.commit()
        
        return existing_project
    
    except Exception as e :
        logging.error("eerror while inserting into table!")
        logging.error(f"Error: {e}")
        db.session.rollback()
        return False


def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file,sheet_name=0)
    return df


@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get('project_name')
    if project_name:
        existing_project = Project.query.filter_by(name=project_name).first()
        if existing_project:
            return jsonify({'error': 'Project already exists.'}), 400
        else:
            new_project = Project.create(name=project_name)
            if new_project:
                return jsonify({'id': new_project.id, 'name': new_project.name}), 201
            else:
                return jsonify({'error': 'Failed to create project.'}), 500
    else:
        return jsonify({'error': 'Missing project_name.'}), 400

        
        
@app.route('/update_project/<int:project_id>' , methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    new_name = data.get('name')
    if new_name:
        updated_project = Project.update(project_id,new_name)
        if updated_project:
            return jsonify({'id' : updated_project.id , 'name' : updated_project.name}),200
        
        return jsonify({'error' : 'Prompt not found.'}), 404
    return jsonify({'error': 'New Prompt name is missing.'}),400



@app.route('/delete_project/<int:project_id>', methods=['DELETE'])

def delete_project(project_id):
    deleted = Project.delete(project_id)
    if deleted:
        return jsonify({'message': 'Prompt deleted successfully.'}),200
    
    else:
         return jsonify({'error:' 'Project not found.'}),404
    


if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        sucess = insert_into_the_table(df)
        if sucess:
            print("data inserted successfully")

        else:
            print("Failed to insert data")

    app.run(debug=True)        

