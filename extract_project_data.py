import pandas as pd
import psycopg2 as pg

def insert_to_the_table(df, db_conn):
    conn = pg.connect(**db_conn)

    try:
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            app = row['Application']
            
            cur.execute("SELECT name FROM jerish.projects WHERE name = %s", (app,))
            existing_record = cur.fetchone()
            if existing_record:
                continue
            
            query = "INSERT INTO jerish.projects(name) VALUES (%s)"
            cur.execute(query, (app,))
        conn.commit()
        return True  # Indicate success
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
        return False  # Indicate failure
    finally:
        cur.close()
        conn.close()

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df
