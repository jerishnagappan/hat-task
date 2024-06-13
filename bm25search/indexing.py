import pysolr
import pandas as pd

excel_data = pd.read_parquet('/Users/jerish.nagappan/Documents/solr/sample_embedding.parquet')


solr_core_url = "http://localhost:8888/solr/play"
solr = pysolr.Solr(solr_core_url, always_commit=True)


solr_docs = []
for index, row in excel_data.iterrows():
    doc = {
        "patnum": str(row['patnum']),
        "vector": row['title_abstract_text_all_claims_text_embedding_3_small_512'].tolist(),
        "title": row['title'],
        "primary_cpc": str(row['primary_cpc']),
        "publication_date": row['publication_date']
    }
    solr_docs.append(doc)

solr.add(solr_docs)
print("Documents inserted successfully.")

