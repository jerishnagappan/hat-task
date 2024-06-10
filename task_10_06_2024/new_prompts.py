import pandas as pd
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Project, Prompt
import configparser
import logging

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)

logging.basicConfig(filename='appssss.log', level=logging.INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db.init_app(app)




# @app.route('/prompt', methods=['POST', 'PUT', 'DELETE'])
# def handle_prompt():
#     if request.method == 'POST':
#         data = request.get_json()
#         project_name = data.get('project_name')
#         prompt_name = data.get('prompt_name')
#         if project_name and prompt_name:
#             project = Project.query.filter_by(name=project_name).first()
#             if project:
#                 created_prompt = Prompt.create(name=prompt_name, project_id=project.id)
#                 if created_prompt:
#                     return jsonify({'id': created_prompt.id, 'name': created_prompt.name}), 201
#             return jsonify({'error': 'Project not found.'}), 404
#         return jsonify({'error': 'Missing project_name or prompt_name.'}), 400

#     elif request.method == 'PUT':

#         data = request.get_json()
#         prompt_id = data.get('prompt_id')
#         new_name = data.get('name')
#         if prompt_id and new_name:
#             updated_prompt = Prompt.update(prompt_id, new_name)
#             if updated_prompt:
#                 return jsonify({'id': updated_prompt.id, 'name': updated_prompt.name}), 200
#             else:
#                 return jsonify({'error': 'Prompt not found.'}), 404
#         return jsonify({'error': 'Missing prompt_id or name.'}), 400

#     elif request.method == 'DELETE':
        
#         data = request.get_json()
#         prompt_id = data.get('jeri')
#         if prompt_id:
#             deleted_prompt = Prompt.delete(prompt_id)
#             if deleted_prompt:
#                 return jsonify({'message': 'Prompt deleted successfully.'}), 200
#             else:
#                 return jsonify({'error': 'Prompt not found.'}), 404
#         return jsonify({'error': 'Missing prompt_id.'}), 400
    


@app.route('/project/<string:project_name>', methods=['POST'])
def handle_project(project_name):
    data = request.get_json()
    
    
    action = data.get('action')
    if not action:
        return jsonify({'error': 'Action parameter is missing.'}), 400

    if action == 'create':
        
        new_project_name = data.get('new_project_name')
        if not new_project_name:
            return jsonify({'error': 'New project name is missing.'}), 400
        existing_project = Project.query.filter_by(name=new_project_name).first()
        if existing_project:
            return jsonify({'error': 'Project already exists.'}), 400
        else:
            new_project = Project(name=new_project_name)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'id': new_project.id, 'name': new_project.name}), 201

    elif action == 'update':
    
        new_name = data.get('new_name')
        if not new_name:
            return jsonify({'error': 'New project name is missing.'}), 400
        project = Project.query.filter_by(name=project_name).first()
        if project:
            project.name = new_name
            db.session.commit()
            return jsonify({'id': project.id, 'name': project.name}), 200
        return jsonify({'error': 'Project not found.'}), 404

    elif action == 'delete':
    
        project = Project.query.filter_by(name=project_name).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully.'}), 200
        return jsonify({'error': 'Project not found.'}), 404

    else:
        return jsonify({'error': 'Invalid action.'}), 400


def insert_to_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            project = Project.query.filter_by(name=app).first()
            if project:
                Prompt.create(name=app, project_id=project.id)
        db.session.commit()
        return True
    
    except Exception as e:
        logging.error("Error while inserting into table!")
        logging.error(f"Error: {e}")
        db.session.rollback()
        return str(e)

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df     

if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        success = insert_to_the_table(df)
        if success == True:
            print("Data inserted successfully.")
        else:
            print(f"Failed to insert data. Error: {success}")

    app.run(debug=True)
