import PyPDF3

with open('/Users/jerish.nagappan/Documents/GEMINI KEY/pdf_files_scan_create_reducefilesize.pdf', 'rb') as pdffileobj:
    
    pdfreader = PyPDF3.PdfFileReader(pdffileobj)
    

    all_text = ""
    
    
    for page_num in range(pdfreader.numPages):
        try:
    
            page = pdfreader.getPage(page_num)
            
            text = page.extractText()
        
            all_text += text
        except Exception as e:
            print(f"Error extracting text from page {page_num + 1}: {e}")

    with open("/Users/jerish.nagappan/Documents/GEMINI KEY/pdf_files_scan_create_reducefilesize.txt", "w") as file1:
        file1.write(all_text)


# from bs4 import BeautifulSoup

# # Read HTML file
# with open("/Users/jerish.nagappan/Documents/GEMINI KEY/view-source_https___www.sec.gov_Archives_edgar_data_1604477_000119312523302228_d199412d8k.htm", "r", encoding="utf-8") as file:
#     html_content = file.read()

# # Parse HTML
# soup = BeautifulSoup(html_content, "html.parser")

# # Remove script and style tags and their contents
# for script in soup(["script", "style"]):
#     script.extract()

# # Extract text
# text_content = soup.get_text(strip=True)

# # Print or save the extracted text
# print(text_content)



