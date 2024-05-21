from insert_project_data import insert_to_the_table, get_data_from_excel

# Define your database connection parameters
db_conn = {
    "host": 'localhost',
    "dbname": 'jerish',
    "user": 'jerish.nagappan',
    "password": '1234', 
    "port": 5432,
}

# Get data from Excel
excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
df = get_data_from_excel(excel_file_path)



# Insert data into the table
success = insert_to_the_table(df, db_conn)
if success:
    print("Data inserted successfully.")
else:
    print("Failed to insert data.")
