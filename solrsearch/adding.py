import pandas as pd
import pysolr

excel_data = pd.read_excel('/Users/jerish.nagappan/Documents/solr/sample_1k_pats.xlsx')

solr_docs = []
for index, row in excel_data.iterrows():
    doc = {
        "id": str(row['pat_id']),  
        "patum": str(row['patnum']),
        "title": str(row['title']),
        "abstract": str(row['abstract_text']),
        "claim": str(row['claim_text'])
    }
    solr_docs.append(doc)

solr_core_url = "http://localhost:8888/solr/mycollection"


solr = pysolr.Solr(solr_core_url, always_commit=True)


solr.add(solr_docs)
print("Documents indexed successfully.")

search_query = 'title :"Makeup And Breakout System For Horizontal Directional Drilling"'
results = solr.search(search_query)
print("Search Results:")
for result in results:
    print(result)
