# from google_patent_scraper import scraper_class
# import ssl
# import json

# ssl._create_default_https_context = ssl._create_unverified_context


# from google_patent_scraper import scraper_class

# scraper = scraper_class()


# patent_number = 'CN105069156A'

# try:

#     err, soup, url = scraper.request_single_patent(patent_number)

#     if not err:
        
#         parsed_data = scraper.get_scraped_data(soup, patent_number, url)
        
#         if 'title' in parsed_data:
#             title = parsed_data['title']
#             print(f"Title of {patent_number}: {title}")
#         else:
#             print(f"Title not found for {patent_number}")
#     else:
#         print(f"Failed to fetch patent {patent_number}: {err}")

# except Exception as e:
#     print(f"Error occurred: {str(e)}")




from google_patent_scraper import scraper_class
import ssl
from bs4 import BeautifulSoup
import requests

ssl._create_default_https_context = ssl._create_unverified_context

# scraper = scraper_class()
# patent_number = 'CN105069156A'

# try:
#     err, soup, url = scraper.request_single_patent(patent_number)

#     if not err:
#         # Parse HTML using BeautifulSoup
#         soup = BeautifulSoup(soup, 'html.parser')
        
#         # Find patent title
#         title_tag = soup.find('title')
#         if title_tag:
#             title = title_tag.text.strip()
#             print(f"Title of {patent_number}: {title}")
#         else:
#             print(f"Title not found for {patent_number}")
#     else:
#         print(f"Failed to fetch patent {patent_number}: {err}")

# except Exception as e:
#     print(f"Error occurred: {str(e)}")




# from google_patent_scraper import scraper_class


# scraper=scraper_class(return_abstract=True)  


# patent_1 = 'US7742806'
# err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)


# patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)


# print(patent_1_parsed['abstract_text'])



import requests
from bs4 import BeautifulSoup

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

def main():
    patent_number = 'US7742806'
    patent_title = fetch_patent_title(patent_number)
    if patent_title:
        print(f"Title of {patent_number}: {patent_title}")
    else:
        print(f"Title not found for {patent_number}")

if __name__ == '__main__':
    main()

