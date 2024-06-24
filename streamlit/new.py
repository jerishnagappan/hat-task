
import psycopg2
import ssl
import json
from google_patent_scraper import scraper_class


db_config = {
    'dbname': 'jerish',
    'user': 'jerish.nagappan',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_config)
print("Connected to PostgreSQL")

    # Create a cursor
cur = conn.cursor()


def insert_into_table(pat_full_json_data):

    insert_query = """
                INSERT INTO patents (
                    title, application_number, inventor_name, assignee_name_orig,
                    assignee_name_current, pub_date, filing_date, priority_date,
                    grant_date, forward_cites_no_family, forward_cites_yes_family,
                    backward_cites_no_family, backward_cites_yes_family
                ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    # print(pat_full_json_data['pub_date'])
    # print(type(pat_full_json_data['pub_date']))
    # print(pat_full_json_data['filing_date'])
    # print(pat_full_json_data['priority_date'])
    # print(pat_full_json_data['inventor_name'])
    # print(pat_full_json_data['grant_date'])
    # print(pat_full_json_data['backward_cites_yes_family'])
    # print(type(pat_full_json_data['backward_cites_yes_family']))
    
    

  



def get_pat_data(patnum):
    ssl._create_default_https_context = ssl._create_unverified_context
    scraper = scraper_class()
    err, soup, url = scraper.request_single_patent(patnum)
    patent_number_parsed = scraper.get_scraped_data(soup,patnum,url)
    return patent_number_parsed


# patent_number = 'US10987654B2'
# patent_number = 'US11020375B2'
pat_list = ['US10987654B2','US11020375B2']

for i in pat_list:
    pat_data = get_pat_data(i)
    insert_into_table(pat_data)
    print('\n\n\n\n\n\n\n\n\n')















rom flask import Blueprint, jsonify, request
from your_project.app.models.patent import Patent
from your_project.app.schemas import PatentSchema

patents_bp = Blueprint('patents', __name__)

patent_schema = PatentSchema()
patents_schema = PatentSchema(many=True)

@patents_bp.route('/patents', methods=['GET'])
def get_patents():
    try:
        patents = Patent.query.all()
        result = patents_schema.dump(patents)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
