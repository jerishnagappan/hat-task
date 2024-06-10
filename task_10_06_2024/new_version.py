import pandas as pd
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import logging
from models import db, Prompt, Version  
config = configparser.ConfigParser()
config.read('confi.ini')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
db.init_app(app)

logging.basicConfig(filename='app.log', level=logging.INFO)



@app.route('/version/<string:version_id>', methods=['POST'])
def handle_version(version_id):
    data = request.get_json()
    action = data.get('action')

    if action == 'create':
        app_name = data.get('app_name')
        prompt_text = data.get('prompt_text')
        existing_prompt = Prompt.query.filter_by(name=app_name).first()
        if existing_prompt:
            new_version = Version.create(prompt_id=existing_prompt.id, prompt_text=prompt_text)
            if new_version:
                return jsonify({'id': new_version.id, 'prompt_text': new_version.prompt_text}), 201
        return jsonify({"error": "Failed to create version."}), 400

    elif action == 'update':
        new_prompt_text = data.get('new_prompt_text')
        if new_prompt_text:
            updated_version = Version.update(version_id, new_prompt_text)
            if updated_version:
                return jsonify({'id': updated_version.id, 'prompt_text': updated_version.prompt_text}), 200
            return jsonify({"error": "Version not found."}), 404
        return jsonify({"error": "New prompt text is missing."}), 400

    elif action == 'delete':
        deleted_version = Version.delete(version_id)
        if deleted_version:
            return jsonify({"message": "Version deleted successfully."}), 200
        return jsonify({"error": "Version not found."}), 404

    else:
        return jsonify({"error": "Invalid action."}), 400

if __name__ == '__main__':
    app.run(debug=True)




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







