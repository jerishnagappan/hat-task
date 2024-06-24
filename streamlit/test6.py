from google_patent_scraper import scraper_class
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# # ~ Initialize scraper class ~ #
# scraper=scraper_class() 

# # ~~ Scrape patents individually ~~ #
# patent_1 = 'US2668287A'
# patent_2 = 'US266827A'
# err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)
# err_2, soup_2, url_2 = scraper.request_single_patent(patent_2)

# # ~ Parse results of scrape ~ #
# patent_1_parsed = scraper.process_patent_html(soup_1,patent_1,url_1)

# print(patent_1_parsed)



from google_patent_scraper import scraper_class

scraper=scraper_class(return_abstract=True)   


patent_1 = 'US7742806'

err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)


patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)


print(patent_1_parsed['abstract_text'])

