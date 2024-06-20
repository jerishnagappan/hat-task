
import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_config = {
    'dbname': 'jerish',
    'user': 'jerish.nagappan',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# SQLAlchemy setup
Base = declarative_base()

class Patent(Base):
    __tablename__ = 'patents'

    id = Column(Integer, primary_key=True)
    patnum = Column(String)
    title = Column(String)
    inventor_name = Column(String)
    application_number = Column(String)
    assignee_name_current = Column(String)
    pub_date = Column(String)
    filing_date = Column(String)
    priority_date = Column(String)
    grant_date = Column(String)
    backward_cites_yes_family = Column(String)
    backward_cites_no_family  = Column(String)
    forward_cites_yes_family = Column(String)
    forward_cites_no_family = Column(String)
    assignee_name_orig = Column(String)



engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")
Session = sessionmaker(bind=engine)
session = Session()

def fetch_patent_details(patnums):
    patents = session.query(Patent).filter(Patent.patnum.in_(patnums)).all()
    return patents

st.title('Patent Details Management')

operation = st.selectbox('Operation', ['Get Patent Details'])

if operation == 'Get Patent Details':
    patnums = st.text_input('Enter patent numbers (comma-separated)')
    if st.button('Get Details'):
        patnums_list = [p.strip() for p in patnums.split(',')]
        patents = fetch_patent_details(patnums_list)
        if patents:
            st.write("Patent Details:")
            table_data = []
            for patent in patents:
                table_row = {
                    'Patent Number': patent.patnum,
                    'Title': patent.title,
                    'Inventor Name': patent.inventor_name,
                    'Application_number' : patent.application_number,
                    'Assignee_name_current' : patent.assignee_name_current,
                    'Pub_date' : patent.pub_date,
                    'Filing_date' : patent.filing_date,
                    'Assignee_name_orig' : patent.assignee_name_orig,
                    'Grant_date' : patent.grant_date,
                    'Priority_date': patent.priority_date,
                    'Forward_cities_no_family': patent.forward_cites_no_family,
                    'Forward_cities_yes_family': patent.forward_cites_yes_family,
                    'Back_ward_cities_yes_family': patent.backward_cites_yes_family,
                    'Back_ward_cities_no_family': patent.backward_cites_no_family



                }
                table_data.append(table_row)
            st.table(table_data)
        else:
            st.write("No patents found with the provided numbers.")




# #title                     | patent
# application_number        | "2fefe"
# inventor_name             | "[{\"inventor_name\": \"nent\"}, {\"inventor_name\": \"indi\"}]"
# assignee_name_orig        | "[{\"assignee_name\": \"Nippon Denko Co Ltd\"}]"
# assignee_name_current     | "[]"
# pub_date                  | 2019-02-07
# filing_date               |
# priority_date             |
# grant_date                | 2021-04-27
# forward_cites_no_family   | {}
# forward_cites_yes_family  | {}
# backward_cites_no_family  | {}
# backward_cites_yes_family | {}
# id                        | 9
# patnum                    | US10987654B2


#st.table(table_data, headers=['Patent Number', 'Title', 'Inventor Name'])