import insert_prompt 


db_conn = {
    "host": 'localhost',
    "dbname": 'jerish',
    "user": 'jerish.nagappan',
    "password": '1234', 
    "port": 5432,
}

try:
    conn = insert_prompt.establish_connection(db_conn)
    df1 = insert_prompt.get_data_from_excel('/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx')
    df2 = insert_prompt.get_project_id(conn)

    final_df = insert_prompt.merge_data(df1, df2)

    if not final_df.empty:
        insert_prompt.insert_to_the_table(final_df, conn)
    else:
        print("DataFrame is empty. No data to insert.")
except Exception as e:
    print("An error occurred while processing data:")
    print(e)
