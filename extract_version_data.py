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


def insert_to_version_table(df):
    try:
        cur = conn.cursor()
        for index, row in df.iterrows():
            query = "INSERT INTO jerish.versions(prompt_id, prompt_text) VALUES (%s, %s)"
            cur.execute(query, (row['id'], row['Prompt']))
        conn.commit()
        print("Data inserted into versions table successfully.")
    except Exception as e:
        print("Error while inserting into versions table!")
        print(f"Error: {e}")
    finally:
        cur.close()

def get_prompt_id():
    query = "SELECT id, name FROM jerish.prompts"
    df = pd.read_sql_query(query, conn)
    return df

def get_data_from_excel():
    excel_file = /Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
    df = pd.read_excel(excel_file, sheet_name=0)
    return df

try:
    df1 = get_data_from_excel()
    df2 = get_prompt_id()

    
    final_df = pd.merge(df1, df2, left_on='Application', right_on='name', how='inner')

    
    prompt_df = final_df[['id', 'name']].copy()
    version_df = final_df[['id', 'Prompt']].copy()


    

    # Insert data into version table
    if not version_df.empty:
        insert_to_version_table(version_df)

except Exception as e:
    print("An error occurred while processing data:")
    print(e)
