# from insert_project import insert_to_the_table, get_data_from_excel

# db_conn = {
#     "host": 'localhost',
#     "dbname": 'jerish',
#     "user": 'jerish.nagappan',
#     "password": '1234', 
#     "port": 5432,
# }

# excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
# df = get_data_from_excel(excel_file_path)



# success = insert_to_the_table(df, db_conn)
# if success:
#     print("Data inserted successfully.")
# else:
#     print("Failed to insert data.")




import psycopg2 as pg
from insert_project import insert_to_the_table, get_data_from_excel
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
