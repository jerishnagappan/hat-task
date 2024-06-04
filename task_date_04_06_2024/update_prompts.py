
import psycopg2 as pg
from insert_prompts import insert_to_the_table, get_data_from_excel
from configparser import ConfigParser

def load_connection_info(ini_filename: str) -> dict:
    parser = ConfigParser()
    parser.read(ini_filename)
    return dict(parser['postgresql'])

# Load connection info from config.ini
config_file = "/Users/jerish.nagappan/Documents/Training/Project/config.ini"
db_conn = load_connection_info(config_file)


conn = pg.connect(**db_conn)

    # Read data from Excel file
excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
df = get_data_from_excel(excel_file_path)



sucess = insert_to_the_table(df,db_conn)
if sucess:
    print("data inserted successfully")

else:
    print("failed to insert")   









    # Get project IDs from the database
    # df2 = get_project_id(conn)

    # # Merge dataframes
    # final_df = pd.merge(df1, df2, left_on='Application', right_on='name', how='inner')
    
    # Insert data into the database
#     if not final_df.empty:
#         insert_to_the_table(final_df, conn)
#     else:
#         print("DataFrame is empty. No data to insert.")
# except Exception as e:
#     print("An error occurred while processing data:")
#     print(e)