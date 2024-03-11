import csv
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import io
import pprint
import pandas as pd

url = "https://www.deccanchronicle.com/technology"

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")
articles = soup.find_all("div", class_="col-lg-3 col-sm-6 grid-margin mb-5 mb-sm-2")

articles_data = []

for article in articles:
    title = article.find("h5", class_="font-weight-bold mt-3 grid-heading").text.strip()
    url1 = article.find("a")["href"]
    if not url1.startswith("http"):
            url1 = "https://www.deccanchronicle.com" + url1

    articles_data.append([title, url1])

fieldnames = ["title", "url"]

try:
    with open("toparticles.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in articles_data:
            writer.writerow({"title": data[0], "url": data[1]})

except IOError:
    print("I/O error:", sys.exc_info()[0])
    pass
except:
    print("Unexpected error:", sys.exc_info()[0])
    pass

print("Scraping completed.\n")

with io.open('toparticles.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    rows = list(reader)

#pprint.pprint(rows)


# Read the existing CSV file
df = pd.read_csv('toparticles.csv')

# Define a function to extract content from a URL
def extract_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text content of the article
    content = soup.find('div', {'class': 'story_content details-story-wrapper details-content-story article_cont_size'})
    if content:
        return content.get_text()
    else:
        return ''

# Define a function to extract content and add it to the DataFrame row
def add_content(row):
    row['content'] = extract_content(row['url'])
    return row

# Apply the function to each row in the DataFrame and save the results
df = df.apply(add_content, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('toparticles_updated.csv', index=False)