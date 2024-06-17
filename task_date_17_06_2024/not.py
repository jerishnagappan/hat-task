import psycopg2
import ssl
from google_patent_scraper import scraper_class
import json

# Database configuration
db_config = {
    'dbname': 'jerish',
    'user': 'jerish.nagappan',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

def insert_into_table(cur, conn, pat_full_json_data):
    insert_query = """
        INSERT INTO patents (
            title, application_number, inventor_name, assignee_name_orig,
            assignee_name_current, pub_date, filing_date, priority_date,
            grant_date, forward_cites_no_family, forward_cites_yes_family,
            backward_cites_no_family, backward_cites_yes_family
        ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cur.execute(insert_query, (
            pat_full_json_data.get('title'),
            pat_full_json_data.get('application_number'),
            json.dumps(pat_full_json_data.get('inventor_name', {})),
            json.dumps(pat_full_json_data.get('assignee_name_orig', {})),
            json.dumps(pat_full_json_data.get('assignee_name_current', {})),
            pat_full_json_data.get('pub_date'),
            pat_full_json_data.get('filing_date'),
            pat_full_json_data.get('priority_date'),
            pat_full_json_data.get('grant_date'),
            json.dumps(pat_full_json_data.get('forward_cites_no_family', {})),
            json.dumps(pat_full_json_data.get('forward_cites_yes_family', {})),
            json.dumps(pat_full_json_data.get('backward_cites_no_family', {})),
            json.dumps(pat_full_json_data.get('backward_cites_yes_family', {}))
        ))
        conn.commit()
        print(f"Data inserted successfully for patent {pat_full_json_data.get('application_number')}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting data for patent {pat_full_json_data.get('application_number')}: {e}")

def get_pat_data(patnum):
    ssl._create_default_https_context = ssl._create_unverified_context
    scraper = scraper_class()
    err, soup, url = scraper.request_single_patent(patnum)
    patent_data = scraper.get_scraped_data(soup, patnum, url)
    return patent_data

def main():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        print("Connected to PostgreSQL")

        cur = conn.cursor()

        pat_list = ['US10987654B2', 'US11020375B2']

        for patent_number in pat_list:
            pat_data = get_pat_data(patent_number)
            insert_into_table(cur, conn, pat_data)

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        if conn is not None:
            conn.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()











