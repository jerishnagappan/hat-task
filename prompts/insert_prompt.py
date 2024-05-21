import pandas as pd
import psycopg2 as pg

def establish_connection(db_conn):
    return pg.connect(**db_conn)

def get_project_id(conn):
    query = "SELECT id, name FROM jerish.projects"
    df = pd.read_sql_query(query, conn)
    return df

def insert_to_the_table(df, conn):
    try:
        cur = conn.cursor()
        for index, row in df.iterrows():
            query = "INSERT INTO jerish.prompts(project_id, name) VALUES (%s, %s)"
            cur.execute(query, (row['id'], row['Application'],))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
    finally:
        cur.close()

def get_data_from_excel(file_path):
    df = pd.read_excel(file_path, sheet_name=0)
    return df

def merge_data(df1, df2):
    final_df = pd.merge(df1, df2, left_on='Application', right_on='name', how='inner')
    return final_df
