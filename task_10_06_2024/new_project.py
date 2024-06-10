import pandas as pd
from flask import Flask, request, jsonify
from models import db, Project
import configparser
import logging

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db.init_app(app)

logging.basicConfig(filename='and.log', level=logging.INFO)

def insert_into_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            existing_project = Project.query.filter_by(name=app).first()
            if not existing_project:
                new_project = Project(name=app)
                db.session.add(new_project)
        db.session.commit()
        return True
    except Exception as e:
        logging.error("Error while inserting into table!")
        logging.error(f"Error: {e}")
        db.session.rollback()
        return False

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df 




@app.route('/project/<int:project_id>', methods=['POST'])
def handle_project(project_id):
    data = request.get_json()
    
    # Check if 'action' is provided in the request data
    action = data.get('action')
    if not action:
        return jsonify({'error': 'Action parameter is missing.'}), 400

    if action == 'create':
        
        project_name = data.get('project_name')
        if not project_name:
            return jsonify({'error': 'Project name is missing.'}), 400
        existing_project = Project.query.filter_by(name=project_name).first()
        if existing_project:
            return jsonify({'error': 'Project already exists.'}), 400
        else:
            new_project = Project(name=project_name)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'id': new_project.id, 'name': new_project.name}), 201

    elif action == 'update':
        
        new_name = data.get('new_name')
        if not new_name:
            return jsonify({'error': 'New project name is missing.'}), 400
        project = Project.query.get(project_id)
        if project:
            project.name = new_name
            db.session.commit()
            return jsonify({'id': project.id, 'name': project.name}), 200
        return jsonify({'error': 'Project not found.'}), 404

    elif action == 'delete':
        
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully.'}), 200
        return jsonify({'error': 'Project not found.'}), 404

    else:
        return jsonify({'error': 'Invalid action.'}), 400

if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        success = insert_into_the_table(df)
        if success:
            print("Data inserted successfully.")
        else:
            print("Failed to insert data.")

    app.run(debug=True)














