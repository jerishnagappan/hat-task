from bs4 import BeautifulSoup
import html2text


html_file_path = "/Users/jerish.nagappan/Documents/GEMINI KEY/view-source_https___www.sec.gov_Archives_edgar_data_1604477_000119312523302228_d199412d8k.htm"  # Replace with the full path to your HTML file

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract text content while preserving CSS styles
html_text = soup.get_text()

plain_text = html2text.html2text(html_text)

# Print the extracted plain text
print(plain_text)
