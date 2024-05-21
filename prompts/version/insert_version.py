import pandas as pd
import psycopg2 as pg

db_conn = {
    "host": 'localhost',
    "dbname": 'jerish',
    "user": 'jerish.nagappan',
    "password": '1234',
    "port": 5432,
}
conn = pg.connect(**db_conn)

def get_prompt_id():
    query = "SELECT id, name FROM jerish.projects"
    df = pd.read_sql_query(query, conn)
    return df

def insert_to_the_table(df):
    try:
        cur = conn.cursor()

        print("Columns in DataFrame:")
        print(df.columns)

        print("DataFrame head:")
        print(df.head())

        for index, row in df.iterrows():
            query = f"INSERT INTO jerish.versions(prompt_id,prompt_text) VALUES (%s,%s)"
            cur.execute(query, (row['id'], row['Prompt'],))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
    finally:
        cur.close()
        # conn.close()  # No need to close connection here

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df
