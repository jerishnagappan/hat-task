import re
import json
import requests
import pdfplumber
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime  


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pdf_text = ''
        for page in pdf.pages:
            pdf_text += page.extract_text()
    return pdf_text


def parse_resume(ocr_text):
    lines = ocr_text.split('\n')
    name = ''
    email = ''
    phone = ''
    dob = ''
    experience = ''
    current_company = ''
    college = ''
    skills = []

   
    in_skills_section = False  

    
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'

    for line in lines:
        line = line.strip()

        
        if not phone:
            match = re.search(phone_pattern, line)
            if match:
                phone = match.group(0)

        
        if not email and ('Email' in line or '@' in line):
            email = line

        
        if not dob and ('DOB' in line or 'Date of Birth' in line):
            
            dob_value = line.split(':')[-1].strip()
            try:
                datetime.strptime(dob_value, '%d/%m/%Y')
                dob = dob_value
            except ValueError:
                dob = ''

        
        if 'Experience' in line or 'Years of Experience' in line:
            experience = line

        
        if 'Current Company' in line or 'Company' in line:
            current_company = line

        
        if 'College' in line or 'University' in line:
            college = line

        
        if 'Skills' in line or 'Technical Skills' in line:
            in_skills_section = True
            continue

       
        if line and not name:
            name = line

        
        if in_skills_section:
            if line:
                skills.append(line.strip())

    return name, email, phone, dob, experience, current_company, college, skills


def send_request_to_gemini(prompt):
    gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDdQoG3AzuDPkO1o-rxAGmLmQbpIOqo-As'
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        response = requests.post(gemini_url, headers=headers, json=prompt)
        if response.status_code == 200:
            parsed_data = response.json()
            
            if 'text' in parsed_data and parsed_data['text']:
                generated_text = parsed_data['text']
            else:
                generated_text = None  
            return generated_text
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error with API request: {e}")
        return None


def insert_into_postgres(df):
    host = 'localhost'
    port = '5432'
    database = 'jerish'
    user = 'jerish.nagappan'
    password = '1234'
    
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()

       
        for index, row in df.iterrows():
            insert_query = sql.SQL('''
                INSERT INTO resumes (name, email, phone, dob, skills)
                VALUES (%s, %s, %s, %s, %s)
            ''')
            
            
            dob_value = row['DOB'] if row['DOB'] else None
            
            cur.execute(insert_query, (
                row['Name'],
                row['Email'],
                row['Phone'],
                dob_value,
                row['Skills'],
            ))
            conn.commit()
        
        print("Data inserted successfully into PostgreSQL")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting data into PostgreSQL: {error}")
    finally:
        if conn is not None:
            conn.close()


def main():
    
    pdf_file_path = '/Users/jerish.nagappan/Documents/GEMINI KEY/Vg.shibu (CV..).pdf'
    
    
    ocr_text = extract_text_from_pdf(pdf_file_path)
    
    
    name, email, phone, dob, experience, current_company, college, skills = parse_resume(ocr_text)
    
    
    prompt = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Given the resume, fetch the name: {name}, email: {email}, phone: {phone}, dob: {dob}, experience: {experience}, current company: {current_company}, college: {college}, top 5 skills: {', '.join(skills)}, vertica as one of Full stack, Data Engineering, Dev Ops, Manual Testing, Automation."
                    }
                ]
            }
        ]
    }
    
    
    prompt_json = json.dumps(prompt)
    
    
    generated_text = send_request_to_gemini(prompt)
    
    
    df = pd.DataFrame({
        'Name': [name],
        'Email': [email],
        'Phone': [phone],
        'DOB': [dob],
        'Experience': [experience],
        'Current Company': [current_company],
        'College': [college],
        'Skills': [skills],
        'Generated Text': [generated_text]
    })
    
    
    print("DataFrame created:")
    print(df)
    
    
    insert_into_postgres(df)

if __name__ == "__main__":
    main()
