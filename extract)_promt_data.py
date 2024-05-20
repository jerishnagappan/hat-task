import pandas as pd
import psycopg2 as pg

def insert_to_the_table(df):
    db_conn = {
        "host": 'localhost',
        "dbname": 'jerish',
        "user": 'jerish.nagappan',
        "password": '1234', 
        "port": 5432,
    }
    conn = pg.connect(**db_conn)

    try:
        cur = conn.cursor()
        
        print("Columns in DataFrame:")
        print(df.columns)
        
        print("DataFrame head:")
        print(df.head())

        for index, row in df.iterrows():
            app = row['Application']
            
            # Check if the project exists in the database
            cur.execute("SELECT id FROM jerish.prompts WHERE name = %s", (app,))
            existing_record = cur.fetchone()
            if existing_record:
                print(f"Skipping duplicate record: {app}")
                continue
            
            # Insert project into jerish.prompts table
            query = "INSERT INTO jerish.prompts(name) VALUES (%s) RETURNING id"
            cur.execute(query, (app,))
            project_id = cur.fetchone()[0]
            
            # Insert project_id into the dataframe
            df.at[index, 'project_id'] = project_id
        
        conn.commit()
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def get_data_from_excel():
    excel_file = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
    df = pd.read_excel(excel_file, sheet_name=0)
    return df

df = get_data_from_excel()
if not df.empty:
    insert_to_the_table(df)
