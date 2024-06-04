import pandas as pd
import psycopg2 as pg


def establish_connection(db_conn):
    return pg.connect(**db_conn)

def get_project_id(conn, project_name):
    try:
        cur = conn.cursor()
        
        # Query to get the project ID by project name
        query = "SELECT id FROM jerish.projects WHERE name = %s"
        cur.execute(query, (project_name,))
        project_id = cur.fetchone()
        
        if project_id:
            return project_id[0]
        else:
            print(f"Project '{project_name}' does not exist.")
            return None
    except Exception as e:
        print("Error while getting project ID!")
        print(f"Error: {e}")
        return None
    finally:
        cur.close()

def insert_to_the_table(df, db_conn):
    conn = establish_connection(db_conn)

    try:
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            app = row['Application']
            
            # Get project ID
            project_id = get_project_id(conn, app)
            if project_id is None:
                continue
            
            # Insert the prompt into the jerish.prompts table
            query = "INSERT INTO jerish.prompts(project_id, name) VALUES (%s, %s)"
            cur.execute(query, (project_id, app,))
            
        conn.commit()
        return True  
    except Exception as e:
        print("Error while inserting into table!")
        print(f"Error: {e}")
        return False  
    finally:
        cur.close()
        conn.close()

def get_data_from_excel(excel_file):
    df = pd.read_excel(excel_file, sheet_name=0)
    return df 
