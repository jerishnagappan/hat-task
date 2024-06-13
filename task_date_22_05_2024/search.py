import pandas as pd
import pysolr


excel_data = pd.read_parquet('pats_embedding_3_small_512_test_1k_data.parquet')

solr_docs = []
for index,row in excel_data.iterrows():
    doc = {
        "patum" : str(row['patnum']),
        "vector" : row['title_abstract_text_all_claims'].tolist()
    }
    solr_docs.append(doc)

solr_core_url = "http://localhost:8888/solr/jeri"  


solr = pysolr.Solr(solr_core_url,always_commit=True)


solr.add(solr_docs)

print("document Inserted successfull")


excel_data['title_abstract_text_all_claims'].values[0].tolist()[:100]


documents = excel_data['title_abstract_text_all_claims'].values[0].tolist()

results=solr.search("{!knn f=vector topK=3}"+str(documents))
print("Saw {0} result(s).".format(len(results)))
for result in results:
    print(result['id'])







