import pandas as pd
from flask import Flask, jsonify ,request
from flask_sqlalchemy import SQLAlchemy
import configparser
import logging

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)


logging.basicConfig(filename='app.log', level=logging.INFO)

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
        logging.info(f"Created prompt: {name} for project ID: {project_id}")
        return new_prompt
    
    @staticmethod
    def update(prompt_id, new_name):
        prompt = Prompt.query.get(prompt_id)
        if prompt:
            prompt.name = new_name
            db.session.commit()
            logging.info(f"Updated prompt ID: {prompt_id} with new name: {new_name}")
            return prompt
        return None
    
    @staticmethod
    def delete(prompt_id):
        prompt = Prompt.query.get(prompt_id)
        if prompt:
            db.session.delete(prompt)
            db.session.commit()
            logging.info(f"Deleted prompt ID: {prompt_id}")
            return prompt
        return None

def insert_to_the_table(df):
    try:
        for index, row in df.iterrows():
            app = row['Application']
            project = Project.query.filter_by(name=app).first()
            if project:
                Prompt.create(name=app, project_id=project.id)
        db.session.commit()
        return project
    
    except Exception as e:
        logging.error("Error while inserting into table!")
        logging.error(f"Error: {e}")
        db.session.rollback()
        return False

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df 

@app.route('/create_prompt', methods=['POST'])
def create_prompt():
    data = request.get_json()
    project_name = data.get('project_name')
    prompt_name = data.get('prompt_name')
    if project_name and prompt_name:
        project = Project.query.filter_by(name=project_name).first()
        if project:
            created_prompt = Prompt.create(name=prompt_name, project_id=project.id)
            if created_prompt:
                return jsonify({'id': created_prompt.id, 'name': created_prompt.name}), 201
        return jsonify({'error': 'Project not found.'}), 404
    return jsonify({'error': 'Missing project_name or prompt_name.'}), 400




@app.route('/update_prompt/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    data = request.get_json()
    new_name = data.get('name')
    if new_name:
        updated_prompt = Prompt.update(prompt_id, new_name)
        if updated_prompt:
            return jsonify({'id': updated_prompt.id, 'name': updated_prompt.name}), 200
        else:
            return jsonify({'error': 'Prompt not found.'}), 404
    else:
        return jsonify({'error': 'New prompt name is missing.'}), 400

@app.route('/delete_prompt/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    deleted = Prompt.delete(prompt_id)
    if deleted:
        return jsonify({'message': 'Prompt deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Prompt not found.'}), 404

if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        success = insert_to_the_table(df)
        if success:
            print("Data inserted successfully.")
        else:
            print("Failed to insert data.")

    app.run(debug=True)







# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# import configparser
# import logging
# import pandas as pd

# config = configparser.ConfigParser()
# config.read('confi.ini')

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.INFO)

# app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
# db = SQLAlchemy(app)

# class Project(db.Model):
#     __tablename__ = 'projects'
#     __table_args__ = {'schema': 'jerish'}
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True, nullable=False)

# class Prompt(db.Model):
#     __tablename__ = 'prompts'
#     __table_args__ = {'schema': 'jerish'}
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
#     name = db.Column(db.String(255), nullable=False)

#     @staticmethod
#     def create(name, project_id):
#         new_prompt = Prompt(name=name, project_id=project_id)
#         db.session.add(new_prompt)
#         db.session.commit()
#         logging.info(f"Created prompt: {name} for project ID: {project_id}")
#         return new_prompt
    
#     @staticmethod
#     def update(prompt_id, new_name):
#         prompt = Prompt.query.get(prompt_id)
#         if prompt:
#             prompt.name = new_name
#             db.session.commit()
#             logging.info(f"Updated prompt ID: {prompt_id} with new name: {new_name}")
#             return prompt
#         return None
    
#     @staticmethod
#     def delete_by_name(prompt_name):
#         prompt = Prompt.query.filter_by(name=prompt_name).first()
#         if prompt:
#             db.session.delete(prompt)
#             db.session.commit()
#             logging.info(f"Deleted prompt with name: {prompt_name}")
#             return prompt
#         return None

# def insert_to_the_table(df):
#     try:
#         for index, row in df.iterrows():
#             app = row['Application']
#             project = Project.query.filter_by(name=app).first()
#             if project:
#                 Prompt.create(name=app, project_id=project.id)
#         db.session.commit()
#         return project
    
#     except Exception as e:
#         logging.error("Error while inserting into table!")
#         logging.error(f"Error: {e}")
#         db.session.rollback()
#         return False

# def get_data_from_excel(excel_file):
#     df = pd.read_excel(excel_file, sheet_name=0)
#     return df 

# @app.route('/create_prompt', methods=['POST'])
# def create_prompt():
#     data = request.get_json()
#     project_name = data.get('project_name')
#     prompt_name = data.get('prompt_name')
#     if project_name and prompt_name:
#         project = Project.query.filter_by(name=project_name).first()
#         if project:
#             created_prompt = Prompt.create(name=prompt_name, project_id=project.id)
#             if created_prompt:
#                 return jsonify({'id': created_prompt.id, 'name': created_prompt.name}), 201
#         return jsonify({'error': 'Project not found.'}), 404
#     return jsonify({'error': 'Missing project_name or prompt_name.'}), 400

# @app.route('/delete_prompt', methods=['DELETE'])
# def delete_prompt_by_name():
#     data = request.get_json()
#     prompt_name = data.get('prompt_name')
#     if prompt_name:
#         prompt = Prompt.query.filter_by(name=prompt_name).first()
#         if prompt:
#             deleted = Prompt.delete(prompt.id)
#             if deleted:
#                 return jsonify({'message': 'Prompt deleted successfully.'}), 200
#         return jsonify({'error': 'Prompt not found.'}), 404
#     return jsonify({'error': 'Prompt name is missing.'}), 400


# if __name__ == '__main__':
#     with app.app_context():
#         excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
#         df = get_data_from_excel(excel_file_path)
#         success = insert_to_the_table(df)
#         if success:
#             print("Data inserted successfully.")
#         else:
#             print("Failed to insert data.")

#     app.run(debug=True)
