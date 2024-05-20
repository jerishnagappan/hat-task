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
    query= "select id,name from jerish.prompts"
    df = pd.read_sql_query(query,conn)

    return df

def insert_to_the_table(df):

    try:
        cur = conn.cursor()
        
        print("Columns in DataFrame:")
        print(df.columns)
        
        print("DataFrame head:")
        print(df.head())
        
        # df.drop_duplicates(subset=['prompt'], inplace=True)
        for index, row in df.iterrows():

            query = f"INSERT INTO jerish.versions(prompt_id,prompt_text) VALUES (%s,%s)"
            cur.execute(query, (row['id'],row['Prompt'],))
        conn.commit()
        print("Data inserted successfully.")
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




try:
    df1 = get_data_from_excel()
    df2 = get_prompt_id()
    print(df1.columns)
    print(df2.columns)

    final_df = pd.merge(df1, df2, left_on='Application', right_on='name', how='inner')

    print(final_df.columns)
    print(final_df)
    if not final_df.empty:
        insert_to_the_table(final_df)
    else:
        print("DataFrame is empty. No data to insert.")
except Exception as e:
    print("An error occurred while processing data:")
    print(e)
# hat-task
