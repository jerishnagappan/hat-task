import pandas as pd
from insert_version import insert_to_the_table, get_prompt_id, get_data_from_excel

try:
    # Get data from Excel
    excel_file_path = '/Users/jerish.nagappan/Documents/Training/Prompt_Store.xlsx'
    df1 = get_data_from_excel(excel_file_path)

    # Get data from database
    df2 = get_prompt_id()

    print(df1.columns)
    print(df2.columns)

    # Merge dataframes
    final_df = pd.merge(df1, df2, left_on='Application', right_on='name', how='inner')

    print(final_df.columns)
    print(final_df)

    if not final_df.empty:
        # Insert merged data into the table
        insert_to_the_table(final_df)
    else:
        print("DataFrame is empty. No data to insert.")
except Exception as e:
    print("An error occurred while processing data:")
    print(e)
