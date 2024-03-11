from bs4 import BeautifulSoup
import csv
import requests

urlm = "https://economictimes.indiatimes.com/industry/banking-/-finance/banking"  
response = requests.get(urlm)
content = response.content

soup = BeautifulSoup(content, "html.parser")
article_elements = soup.find_all("div", class_="eachStory")

with open("scrap_file1.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Title", "URL"])

    for article_element in article_elements:
        title_element = article_element.find("h3").find("a")
        title = title_element.text.strip()
        url = title_element["href"]
        if not url.startswith("http"):
            url = "https://economictimes.indiatimes.com" + url

        csv_writer.writerow([title, url])

# Read the URLs from the CSV file
with open('scrap_file1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    urls = [row[1] for row in reader]

# Define the function to extract text content from a URL
'''def get_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tag = soup.find('article')
        text_content = article_tag.get_text()

        return text_content
    else:
        print(f'Failed to fetch the URL. Status code: {response.status_code}')
        return ''
        '''
    
def get_content(url):
    if not url.startswith("http"):
        url = "https://economictimes.indiatimes.com" + url

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tag = soup.find('article')
        text_content = article_tag.get_text()
        return text_content
    else:
        print(f'Failed to fetch the URL. Status code: {response.status_code}')
        return ''

# Add the 'page_content' column to the CSV file and write the text content for each URL
'''with open('scrap_file1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    header.append('page_content')

    with open('scrap_file1.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for url in urls:
            text_content = get_content(url)
            writer.writerow([url, text_content])'''

with open('scrap_file1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    header.append('page_content')

    with open('scrap_file1.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for row in reader:
            url = row[1]
            text_content = get_content(url)
            row.append(text_content)
            writer.writerow(row)