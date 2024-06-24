# from google_patent_scraper import scraper_class
# from bs4 import BeautifulSoup
# import requests
# import json
# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context

# # Function to fetch patent title using BeautifulSoup
# def fetch_patent_title(patent_number):
#     url = f"https://patents.google.com/patent/{patent_number}"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             title_tag = soup.find('meta', attrs={'name': 'DC.title'})
#             if title_tag:
#                 return title_tag['content']
#             else:
#                 return None
#         else:
#             print(f"Failed to fetch patent details: {response.status_code}")
#             return None
#     except requests.RequestException as e:
#         print(f"Error fetching patent details: {str(e)}")
#         return None

# def main():
#     scraper = scraper_class()

#     scraper.add_patents('US2668287A')
#     scraper.add_patents('US266827A')

#     scraper.scrape_all_patents()

#     patent_1_parsed = scraper.parsed_patents['US2668287A']
#     patent_2_parsed = scraper.parsed_patents['US266827A']

#     # Check if title is missing for US2668287A and fetch it if necessary
#     if 'title' not in patent_1_parsed:
#         patent_1_parsed['title'] = fetch_patent_title('US2668287A')

#     # Check if title is missing for US266827A and fetch it if necessary
#     if 'title' not in patent_2_parsed:
#         patent_2_parsed['title'] = fetch_patent_title('US266827A')

#     print('Details of US2668287A:', json.dumps(patent_1_parsed, indent=2))
#     print('Details of US266827A:', json.dumps(patent_2_parsed, indent=2))

# if __name__ == '__main__':
#     main()



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
            print(f"Failed to fetch patent details: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching patent details: {str(e)}")
        return None

def insert_into_table(cur, conn, pat_full_json_data, patnum):
    insert_query = """
        INSERT INTO patents (
            patnum, title, application_number, inventor_name, assignee_name_orig,
            assignee_name_current, pub_date, filing_date, priority_date,
            grant_date, forward_cites_no_family, forward_cites_yes_family,
            backward_cites_no_family, backward_cites_yes_family
        ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        # Check if patnum already exists
        cur.execute("SELECT EXISTS(SELECT 1 FROM patents WHERE patnum = %s)", (patnum,))
        exists = cur.fetchone()[0]

        if exists:
            print(f"Patent {patnum} already exists, skipping insertion.")
        else:
            # Fetch title if not present
            if 'title' not in pat_full_json_data:
                pat_full_json_data['title'] = fetch_patent_title(patnum)

            cur.execute(insert_query, (
                patnum,
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
            print(f"Data inserted successfully for patent {patnum}")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting data for patent {patnum}: {e}")

def get_pat_data(patnum):
    ssl._create_default_https_context = ssl._create_unverified_context
    scraper = scraper_class()
    err, soup, url = scraper.request_single_patent(patnum)
    patent_data = scraper.get_scraped_data(soup, patnum, url)    
    return patent_data

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
    pat_list = ['US10987458B2', 'US11020367B2']
    
    scraped_data = scrape_patent_data(pat_list)
    
    for patnum, patent_data in scraped_data.items():
        store_patent_in_db(patnum, patent_data)

if __name__ == "__main__":
    main()
