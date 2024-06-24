from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Patent  
from google_patent_scraper import scraper_class
import ssl
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jerish.nagappan:1234@localhost/jerish'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def insert_into_table(pat_full_json_data, patnum):
    existing_patent = Patent.query.filter_by(patnum=patnum).first()
    

    if existing_patent:
        print(f"Patent {patnum} already exists, skipping insertion.")
    else:
        patent = Patent(
            patnum=patnum,
            title=pat_full_json_data.get('title'),
            application_number=pat_full_json_data.get('application_number'),
            inventor_name=json.dumps(pat_full_json_data.get('inventor_name', {})),
            assignee_name_orig=json.dumps(pat_full_json_data.get('assignee_name_orig', {})),
            assignee_name_current=json.dumps(pat_full_json_data.get('assignee_name_current', {})),
            pub_date=pat_full_json_data.get('pub_date'),
            filing_date=pat_full_json_data.get('filing_date'),
            priority_date=pat_full_json_data.get('priority_date'),
            grant_date=pat_full_json_data.get('grant_date'),
            forward_cites_no_family=json.dumps(pat_full_json_data.get('forward_cites_no_family', {})),
            forward_cites_yes_family=json.dumps(pat_full_json_data.get('forward_cites_yes_family', {})),
            backward_cites_no_family=json.dumps(pat_full_json_data.get('backward_cites_no_family', {})),
            backward_cites_yes_family=json.dumps(pat_full_json_data.get('backward_cites_yes_family', {}))
        )
        db.session.add(patent)
        db.session.commit()
        print(f"Data inserted successfully for patent {patnum}")

def get_pat_data(patnum):
    ssl._create_default_https_context = ssl._create_unverified_context
    scraper = scraper_class()
    err, soup, url = scraper.request_single_patent(patnum)
    patent_data = scraper.get_scraped_data(soup, patnum, url)
    return patent_data

@app.route('/')
def main():
    pat_list = ['US10987654B2', 'US11020375B2']

    for patent_number in pat_list:
        pat_data = get_pat_data(patent_number)
        insert_into_table(pat_data, patent_number)

    return "Data inserted into database!"

if __name__ == "__main__":
    app.run(debug=True)


