import pandas as pd
import psycopg2 as pg


def establish_connection(db_conn):
    return pg.connect(**db_conn)

def get_prompt_id(conn, prompt_name):
    try:
        cur = conn.cursor()
        
        # Query to get the prompt ID by prompt name
        query = "SELECT id FROM jerish.prompts WHERE name ~* %s"
        cur.execute(query, (prompt_name,))
        prompt_id = cur.fetchone()
        
        if prompt_id:
            print('prompt_id: ',prompt_id)
            print('success')
            return prompt_id[0]
        
        else:
            # print(f"Prompt '{prompt_name}' does not exist.")
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()

def insert_to_the_table(df, db_conn):
    conn = establish_connection(db_conn)

    try:
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            prompt = row['Application']
            prompt_text = row['Prompt']
            
            # Get prompt ID
            prompt_id = get_prompt_id(conn, prompt)
            if prompt_id is None:
                continue
            
            # Insert the version into the jerish.versions table
            query = "INSERT INTO jerish.versions(prompt_id, prompt_text) VALUES (%s, %s)"
            cur.execute(query, (prompt_id, prompt_text,))
            
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
