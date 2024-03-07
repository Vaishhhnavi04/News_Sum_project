import csv
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import io
import pprint
import pandas as pd
import os

# URL list
url_list = [
    "https://www.deccanchronicle.com/just-in",
    "https://www.deccanchronicle.com/technology",
    "https://www.deccanchronicle.com/business",
]

for i, url in enumerate(url_list):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.find_all("div", class_="col-lg-3 col-sm-6 grid-margin mb-5 mb-sm-2")

    articles_data = []

    for article in articles:
        title = article.find("h5", class_="font-weight-bold mt-3 grid-heading").text.strip()
        url = urljoin(url, article.find("a")["href"])
        articles_data.append([title, url])

    fieldnames = ["title", "url"]

    try:
        with open(f"scrap_file{i}.csv", "w", newline="", encoding="utf-8") as csvfile:
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

    print(f"Scraping completed for {url}.\n")

    with io.open(f'scrap_file{i}.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    pprint.pprint(rows)

    df = pd.read_csv(f'scrap_file{i}.csv')

    #getting article content/info
    def extract_content(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        content_data = {
            'p_tags': [p.text.strip() for p in soup.find_all('p')],
            'ol_tags': [ol.text.strip() for ol in soup.find_all('ol')],
            'ul_tags': [ul.text.strip() for ul in soup.find_all('ul')],
        }

        return content_data

    
    def add_content(row, content_data):
        row["content_p_tags"] = content_data['p_tags'][:10]
        row["content_ol_tags"] = content_data['ol_tags'][:5]
        row["content_ul_tags"] = content_data['ul_tags'][:5]
        return row

    # apply function to each row 
    content_data = extract_content(url)
    df = df.apply(add_content, axis=1, args=(content_data,))
    df.to_csv(f'scrap_file{i}.csv', index=False)
    
    df_test = pd.read_csv('scrap_file1.csv')
    print(df_test.head(1))

    '''
    df.to_csv(f'scrap_file{i}.csv', index=False)
    print(f"Updated CSV file: scrap_file{i}.csv")
    print("_________________________________________________________________________________________")

    with io.open(f'scrap_file{i}.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        rows = list(reader)'''
    