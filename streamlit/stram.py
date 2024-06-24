
# import streamlit as st
# from sqlalchemy import create_engine, Column, String, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# db_config = {
#     'dbname': 'jerish',
#     'user': 'jerish.nagappan',
#     'password': '1234',
#     'host': 'localhost',
#     'port': '5432'
# }


# Base = declarative_base()

# class Patent(Base):
#     __tablename__ = 'patents'

#     id = Column(Integer, primary_key=True)
#     patnum = Column(String)
#     title = Column(String)
#     inventor_name = Column(String)
#     application_number = Column(String)
#     assignee_name_current = Column(String)
#     pub_date = Column(String)
#     filing_date = Column(String)
#     priority_date = Column(String)
#     grant_date = Column(String)
#     backward_cites_yes_family = Column(String)
#     backward_cites_no_family  = Column(String)
#     forward_cites_yes_family = Column(String)
#     forward_cites_no_family = Column(String)
#     assignee_name_orig = Column(String)



# engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")
# Session = sessionmaker(bind=engine)
# session = Session()

# def fetch_patent_details(patnums):
#     patents = session.query(Patent).filter(Patent.patnum.in_(patnums)).all()
#     return patents

# st.title('Patent Details Management')

# operation = st.selectbox('Operation', ['Get Patent Details'])

# if operation == 'Get Patent Details':
#     patnums = st.text_input('Enter patent numbers (comma-separated)')
#     if st.button('Get Details'):
#         patnums_list = [p.strip() for p in patnums.split(',')]
#         patents = fetch_patent_details(patnums_list)
#         if patents:
#             st.write("Patent Details:")
#             table_data = []
#             for patent in patents:
#                 table_row = {
#                     'Patent Number': patent.patnum,
#                     'Title': patent.title,
#                     'Inventor Name': patent.inventor_name,
#                     'Application_number' : patent.application_number,
#                     'Assignee_name_current' : patent.assignee_name_current,
#                     'Pub_date' : patent.pub_date,
#                     'Filing_date' : patent.filing_date,
#                     'Assignee_name_orig' : patent.assignee_name_orig,
#                     'Grant_date' : patent.grant_date,
#                     'Priority_date': patent.priority_date,
#                     'Forward_cities_no_family': patent.forward_cites_no_family,
#                     'Forward_cities_yes_family': patent.forward_cites_yes_family,
#                     'Back_ward_cities_yes_family': patent.backward_cites_yes_family,
#                     'Back_ward_cities_no_family': patent.backward_cites_no_family



#                 }
#                 table_data.append(table_row)
#             st.table(table_data)
#         else:
#             st.write("No patents found with the provided numbers.")



# from your_project.app.extensions import db
# from your_project.app.models.patent import Patent
# from your_project.test import scrape_patent_data, store_patent_in_db ,get_pat_data 
# import streamlit as st
# from flask import Blueprint, request, jsonify
# # from your_project.app import create_app
# patents_bp = Blueprint('patents', __name__)
# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  

# file_handler = logging.FileHandler('flask_app.log')
# file_handler.setLevel(logging.DEBUG)  

# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)


# logger.addHandler(file_handler)

# @patents_bp.route('/get_patent_details', methods=['GET'])
# def get_patent_details():

#     patnum = request.args.get('patnum')

#     if not patnum:
#         logger.error("No patnum provided in GET request")
        
#         return jsonify({"error": "No patnum provided"}), 40
# def fetch_patent(patnum):
#     try:
#         patent = Patent.query.filter_by(patnum=patnum).first()

#         if patent:
#             logger.info(f"Patent {patnum} found in the database")
#             return patent.to_dict()
#         else:
#             patent_data = get_pat_data(patnum)
#             store_patent_in_db(patnum, patent_data)
#             logger.info(f"Scraped and stored patent data for {patnum}")
#             return patent_data

#     except Exception as e:
#         logger.error(f"Error fetching or storing patent {patnum}: {str(e)}")
#         return {"error": f"Failed to fetch or store patent: {str(e)}"}

# def main():
#     st.title('Patent Details App')

#     patnum = st.text_input('Enter Patent Number:')
    
#     if st.button('Get Patent Details'):
#         if not patnum:
#             st.error("Please enter a patent number.")
#         else:
#             patent_data = fetch_patent(patnum)
#             if 'error' in patent_data:
#                 st.error(patent_data['error'])
#             else:
#                 st.json(patent_data)

# if __name__ == '__main__':
#     main()



# import streamlit as st
# import requests


# def fetch_patent_details(patnum):
#     url = 'http://localhost:5000/patents/get_patent_details'  
#     params = {'patnum': patnum}

#     try:
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch patent details: {response.status_code}")
#     except requests.RequestException as e:
#         st.error(f"Error fetching patent details: {str(e)}")

# def main():
#     st.title('Patent Details App')

#     patnum = st.text_input('Enter Patent Number:')

#     if st.button('Get Patent Details'):
#         if not patnum:
#             st.error("Please enter a patent number.")
#         else:
#             patent_data = fetch_patent_details(patnum)
#             if 'error' in patent_data:
#                 st.error(patent_data['error'])
#             else:
#                 st.json(patent_data)

# if __name__ == '__main__':
#     main()




# import streamlit as st
# import requests

# def fetch_patent_details(patnum):
#     url = 'http://localhost:5000/patents/get_patent_details'
#     params = {'patnum': patnum}

#     try:
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch patent details: {response.status_code}")
#     except requests.RequestException as e:
#         st.error(f"Error fetching patent details: {str(e)}")

# def main():
#     st.title('Patent Details App')

#     patnum = st.text_input('Enter Patent Number:')

#     if st.button('Get Patent Details'):
#         if not patnum:
#             st.error("Please enter a patent number.")
#         else:
#             patent_data = fetch_patent_details(patnum)
#             if 'error' in patent_data:
#                 st.error(patent_data['error'])
#             else:
#                 st.header('Patent Details')
#                 st.write(f"Patent Number: {patent_data['patnum']}")
#                 st.write(f"Title: {patent_data['title']}")
#                 st.write(f"Inventor Name: {patent_data['inventor_name']}")
#                 st.write(f"Application Number: {patent_data['application_number']}")
#                 st.write(f"Grant Date: {patent_data['grant_date']}")
#                 st.write(f"Filing_date: {patent_data['filing_date']}")
#                 st.write(f"id:{patent_data['id']}")
#                 st.write(f"Assignnee Name Orig:{patent_data['assignee_name_orig']}")
#                 st.write(f"Backward Cities No Family:{patent_data['backward_cites_no_family']}")
#                 st.write(f"Backward Cities Yes Family:{patent_data['backward_cites_yes_family']}")
#                 st.write(f"Forward Cities Yes Family:{patent_data['forward_cites_yes_family']}")
#                 st.write(f"Forward Cities No family:{patent_data['forward_cites_no_family']}")
#                 st.write(f"Pub Date:{patent_data['pub_date']}")
#                 st.write(f"Priority Date:{patent_data['priority_date']}")

                
        

# if __name__ == '__main__':
#     main()



import streamlit as st
import requests

def fetch_patent_details(patnum):
    url = 'http://localhost:5000/patents/get_patent_details'
    params = {'patnum': patnum}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch patent details: {response.status_code}")
            return {}
    except requests.RequestException as e:
        st.error(f"Error fetching patent details: {str(e)}")
        return {}

def main():
    st.title('Patent Details App')

    patnum = st.text_input('Enter Patent Number:')

    if st.button('Get Patent Details'):
        if not patnum:
            st.error("Please enter a patent number.")
        else:
            patent_data = fetch_patent_details(patnum)
            if 'error' in patent_data:
                st.error(patent_data['error'])
            else:
                st.header('Patent Details')

                
                inventor_name = patent_data.get('inventor_name', [])
                if isinstance(inventor_name, list):
                    inventor_name_str = ', '.join([inventor.get('inventor_name', '') for inventor in inventor_name])
                elif isinstance(inventor_name, str):
                    inventor_name_str = inventor_name  
                else:
                    inventor_name_str = 'N/A'  

                
                table_data = [{
                    'Patent Number': patent_data.get('patnum', 'N/A'),
                    'Title': patent_data.get('title', 'N/A'),
                    'Inventor Name': inventor_name_str,
                    'Application Number': patent_data.get('application_number', 'N/A'),
                    'Grant Date': patent_data.get('grant_date', 'N/A'),
                    'Filing Date': patent_data.get('filing_date', 'N/A'),
                    'ID': patent_data.get('id', 'N/A'),
                    'Assignee Name Orig': patent_data.get('assignee_name_orig', 'N/A'),
                    'Backward Cities No Family': ', '.join(patent_data.get('backward_cites_no_family', [])),
                    'Backward Cities Yes Family': ', '.join(patent_data.get('backward_cites_yes_family', [])),
                    'Forward Cities Yes Family': ', '.join(patent_data.get('forward_cites_yes_family', [])),
                    'Forward Cities No Family': ', '.join(patent_data.get('forward_cites_no_family', [])),
                    'Pub Date': patent_data.get('pub_date', 'N/A'),
                    'Priority Date': patent_data.get('priority_date', 'N/A'),
                    'Abstract': patent_data.get('abstract','N/A')
                }]

                
                st.table(table_data)

if __name__ == '__main__':
    main()




# title                     |
# application_number        |
# inventor_name             | "[{\"inventor_name\": \"none\"}, {\"inventor_name\": \"jeriii\"}]"
# assignee_name_orig        | "[{\"assignee_name\": \"Suzhou Auzone Biological Technology Co Ltd\"}]"
# assignee_name_current     | "[]"
# pub_date                  | "\"2019-03-21\""
# filing_date               |
# priority_date             |
# grant_date                | "2021-06-01"
# forward_cites_no_family   | "[]"
# forward_cites_yes_family  | {}
# backward_cites_no_family  | "[]"
# backward_cites_yes_family | {}
# id                        | 13
# patnum                    | US11020375B2
# -[ RECORD 3 ]------------