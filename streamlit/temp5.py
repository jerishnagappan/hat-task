import psycopg2
import ssl
from google_patent_scraper import scraper_class
import json
from bs4 import BeautifulSoup
import requests


db_config = {
    'dbname': 'jerish',
    'user': 'jerish.nagappan',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

def fetch_patent_title(patent_number):
    url = f"https://patents.google.com/patent/{patent_number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_tag = soup.find('meta', attrs={'name': 'DC.title'})
            if title_tag:
                return title_tag['content']
            else:
                return None
        else:
            print(f"Failed to fetch patent details for {patent_number}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching patent details for {patent_number}: {str(e)}")
        return None

def insert_into_table(cur, conn, pat_full_json_data, patnum):
    insert_query = """
        INSERT INTO patents (
            patnum, title, abstract, application_number, inventor_name, assignee_name_orig,
            assignee_name_current, pub_date, filing_date, priority_date,
            grant_date, forward_cites_no_family, forward_cites_yes_family,
            backward_cites_no_family, backward_cites_yes_family
        ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cur.execute("SELECT EXISTS(SELECT 1 FROM patents WHERE patnum = %s)", (patnum,))
        exists = cur.fetchone()[0]

        if exists:
            print(f"Patent {patnum} already exists, skipping insertion.")
        else:
            # Fetch title and abstract if not present
            if 'title' not in pat_full_json_data:
                pat_full_json_data['title'] = fetch_patent_title(patnum)
            
            if 'abstract' not in pat_full_json_data:
                pat_full_json_data['abstract'] = fetch_patent_abstract(patnum)

            cur.execute(insert_query, (
                patnum,
                pat_full_json_data.get('title'),
                pat_full_json_data.get('abstract'),
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
            print(f"Data inserted successfully for patent {patnum}")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting data for patent {patnum}: {e}")

def get_pat_data(patnum):
    ssl._create_default_https_context = ssl._create_unverified_context
    scraper = scraper_class(return_abstract=True)  # Include abstract in scraped data
    err, soup, url = scraper.request_single_patent(patnum)
    patent_data = scraper.get_scraped_data(soup, patnum, url)    
    return patent_data

def fetch_patent_abstract(patent_number):
    scraper = scraper_class(return_abstract=True)
    err_1, soup_1, url_1 = scraper.request_single_patent(patent_number)
    patent_1_parsed = scraper.get_scraped_data(soup_1, patent_number, url_1)
    return patent_1_parsed['abstract_text'] if 'abstract_text' in patent_1_parsed else None

def scrape_patent_data(pat_list):
    scraped_data = {}
    for patent_number in pat_list:
        scraped_data[patent_number] = get_pat_data(patent_number)
    return scraped_data

def store_patent_in_db(patnum, patent_data):
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        print("Connected to PostgreSQL")

        cur = conn.cursor()

        insert_into_table(cur, conn, patent_data, patnum)  

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL or inserting data: {e}")
    finally:
        if conn is not None:
            conn.close()
            print("PostgreSQL connection is closed")

def main():
    pat_list = ['US10987658B2', 'US11020374B2']
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    try:
        
        for patnum in pat_list:
            cur.execute("SELECT EXISTS(SELECT 1 FROM patents WHERE patnum = %s)", (patnum,))
            exists = cur.fetchone()[0]
            
            if not exists:
                patent_data = get_pat_data(patnum)
                
                if 'title' not in patent_data:
                    patent_data['title'] = fetch_patent_title(patnum)
                
                if 'abstract' not in patent_data:
                    patent_data['abstract'] = fetch_patent_abstract(patnum)
                
                store_patent_in_db(patnum, patent_data)
            else:
                print(f"Patent {patnum} already exists in the database, skipping.")

    except psycopg2.Error as e:
        print(f"Error querying/inserting data: {e}")
    finally:
        if conn is not None:
            conn.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()
