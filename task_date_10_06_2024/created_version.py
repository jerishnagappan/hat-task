import pandas as pd
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import logging

config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)


logging.basicConfig(filename='app.log', level=logging.INFO)

class Prompt(db.Model):
    __tablename__ = 'prompts'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jerish.projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


class Version(db.Model):
    __tablename__ = 'versions'
    __table_args__ = {'schema': 'jerish'}
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey('jerish.prompts.id'), nullable=True)
    prompt_text = db.Column(db.String(255), nullable=False)

    @staticmethod
    def create(prompt_id, prompt_text):
        new_version = Version(prompt_id=prompt_id, prompt_text=prompt_text)
        db.session.add(new_version)
        db.session.commit()
        logging.info(f"Created version: {prompt_text} for project ID: {prompt_id}")
        return new_version
    
    @staticmethod
    def update(version_id, new_prompt_text):
        version = Version.query.get(version_id)
        if version:
            version.prompt_text = new_prompt_text
            db.session.commit()
            logging.info(f"Updated prompt ID: {version_id} with new text: {new_prompt_text}")
            return version  
        return None
    
    @staticmethod
    def delete(version_id):
        version = Version.query.get(version_id)
        if version:
            db.session.delete(version)
            db.session.commit()
            logging.info(f"Deleted version ID: {version_id}")
            return version  
        return None

def insert_to_the_table(df):
    created_objects = []
    try:
        for index, row in df.iterrows():
            app = row['Application']
            prompt_text = row['Prompt']
            existing_prompt = Prompt.query.filter_by(name=app).first()
            if existing_prompt:
                new_version = Version.create(prompt_id=existing_prompt.id, prompt_text=prompt_text)
                created_objects.append(new_version)
            else:
                logging.error(f"Prompt '{app}' not found in the database.")
        db.session.commit()
    except Exception as e:
        logging.error("Error while inserting into table!")
        logging.error(f"Error: {e}")
        db.session.rollback()
    return created_objects

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df 



@app.route('/create_version', methods=['POST'])
def create_version():
    data = request.get_json()
    app_name = data.get('app_name')
    prompt_text = data.get('prompt_text')
    existing_prompt = Prompt.query.filter_by(name=app_name).first()
    if existing_prompt:
        new_version = Version.create(prompt_id=existing_prompt.id, prompt_text=prompt_text)
        if new_version:
            # return jsonify(new_version.serialize()), 201
            return jsonify({'id': new_version.id, 'name': new_version.name}), 201
    return jsonify({"message": "Failed to create version."}), 400

@app.route('/update_version/<int:version_id>', methods=['PUT'])
def update_version(version_id):
    data = request.get_json()
    new_prompt_text = data.get('prompt_text')
    updated_version = Version.update(version_id, new_prompt_text)
    if updated_version:
        return jsonify(updated_version.serialize()), 200
    return jsonify({"message": "Version not found."}), 404

@app.route('/delete_version/<int:version_id>', methods=['DELETE'])
def delete_version(version_id):
    deleted_version = Version.delete(version_id)
    if deleted_version:
        return jsonify({"message": "Version deleted successfully."}), 200
    return jsonify({"message": "Version not found."}), 404

if __name__ == '__main__':
    with app.app_context():
        excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
        df = get_data_from_excel(excel_file_path)
        created_objects = insert_to_the_table(df)
        if created_objects:
            logging.info("Data inserted successfully.")
        else:
            logging.error("Failed to insert data.")

    app.run(debug=True)



