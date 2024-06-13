import streamlit as st
import pysolr
import pandas as pd

def bm25_search(keyword, cpc_filter, limit, solr_core_url):
    solr = pysolr.Solr(solr_core_url)
    query = f"title:*{keyword}*"
    if cpc_filter:
        query += f" AND cpc:{cpc_filter}"
    results = solr.search(q=query, rows=limit)
    return results

def semantic_search(keyword, cpc_filter, limit, solr_core_url, excel_data):
    solr = pysolr.Solr(solr_core_url)
    
    
    query = f"title:*{keyword}* AND "
    
    documents = excel_data['title_abstract_text_all_claims_text_embedding_3_small_512'].values[0].tolist()
    query += f"{{!knn f=vector topK=10 v='{documents}'}}"
    if cpc_filter:
        query += f" AND cpc:{cpc_filter}"

    results = solr.search(q=query, rows=limit)
    return results

st.title("Patent Search")

keyword = st.text_input("Enter Keyword:")
cpc_filter = st.text_input("Enter CPC Filter (optional):")
limit = st.number_input("Limit (K Returns):", min_value=1, max_value=100, value=10)
solr_core_url = st.text_input("Solr Core URL:", "http://localhost:8888/solr/play")

search_method = st.radio("Search Method:", ("BM25", "Semantic"))

if st.button("Search"):
    excel_data = pd.read_parquet('/Users/jerish.nagappan/Documents/solr/sample_embedding.parquet')
    if search_method == "BM25":
        results = bm25_search(keyword, cpc_filter, limit, solr_core_url)
    else:
        results = semantic_search(keyword, cpc_filter, limit, solr_core_url, excel_data)

    
    st.write("Search Results:")
    if results:
        table_data = []
        for idx, result in enumerate(results, start=1):
            sno = idx
            patnum = result.get("patnum", "N/A")
            title = result.get("title", "N/A")
            cpc = result.get("cpc", "N/A")
            score = result.get("score", "N/A")
            table_data.append((sno, patnum, title, cpc, score))

    
        table_data = [("Sno", "Patnum", "Title", "CPC", "Score")] + table_data

        st.table(table_data)
    else:
        st.write("No results found.")















# import streamlit as st

# st.write("""  
# # SImple stock price App
# shown are the  stock closing price and volume of Google!   


# """)

