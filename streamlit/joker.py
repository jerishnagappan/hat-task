# @patents_bp.route('/get_patent_details', methods=['GET'])
# def get_patent_details():
#     patnum = request.args.get('patnum')

#     if not patnum:
#         return jsonify({"error": "No patnum provided"}), 400


#     patent = Patent.query.filter_by(patnum=patnum).first()

#     if patent:
#         return jsonify(patent.to_dict()), 200
#     else:
#         return jsonify({"error": "Patent not found"}), 404




from google_patent_scraper import scraper_class
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context



scraper=scraper_class() 


patent_1 = 'US2668287A'
patent_2 = 'US266827A'
err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)
err_2, soup_2, url_2 = scraper.request_single_patent(patent_2)


patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)
patent_2_parsed = scraper.get_scraped_data(soup_2,patent_2,url_2)