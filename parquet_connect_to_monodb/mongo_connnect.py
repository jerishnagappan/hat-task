import pandas as pd
import json
import pymongo


dff = pd.read_parquet('/Users/jerish_nagappan/Documents/EmailParsing/rent.parquet')


client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['GFG']
collection = db["data"]



json_data = []
for json_str in dff["json_file"]:
    json_data.append(json.loads(json_str))
    
print(len(json_data))
for d in json_data:
    
        collection.insert_many(json_data)
        print(json_data)
        print(" inserted successfully.")
    
