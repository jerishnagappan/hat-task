# search.py

import pysolr
import pandas as pd

def search_documents( execel_data, solr_core_url):
    solr = pysolr.Solr(solr_core_url)

    documents = excel_data['title_abstract_text_all_claims_text_embedding_3_small_512'].values[0].tolist()
    results = solr.search(q='(title: payment system are done properly   {!knn f=vector topK=1 v="'+str(documents)+'"})')


    print(f"Saw {len(results)} result(s).")
    for result in results:
        print(result["title"])

if __name__ == "__main__":
    
    excel_data = pd.read_parquet('/Users/jerish.nagappan/Documents/solr/sample_embedding.parquet')

    #
    solr_core_url = "http://localhost:8888/solr/play"

    
    

    # Search for documents
    search_documents( excel_data, solr_core_url)
