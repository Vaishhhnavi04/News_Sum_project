import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re
import time

class EconomicTimesScraper:
    def __init__(self):
        self.base_url = 'https://economictimes.indiatimes.com'
        self.url_keywords = ['technology', 'tech', 'ai', 'artificial-intelligence', 'machine-learning', 'data-science', 'innovation', 'startup', 'sports', 'marketing', 'finance']
        self.exclude_segments = ['/news/', '/prime', '/stocks/', '/entertainment/']
        self.allowed_domain='economictimes.indiatimes.com'

    def filter_urls_by_keywords(self, links, search_term):
        filtered_links = []
        count = 0
        for link in links:
            if self.allowed_domain not in link:
                continue

            #Skip this URL
            if any(ex_segment in link.lower() for ex_segment in self.exclude_segments):
                continue

            #appending relevant links
            if search_term.lower() in link.lower() and any(keyword.lower() in link.lower() for keyword in self.url_keywords):
                filtered_links.append(link)
                count+=1
                if count==5: 
                    break

        return filtered_links

    #Cleaning extracted text
    def post_processing(self, text):

        text=re.sub(r'[^\x00-\x7F]+', '',text)

        return text

    def fetch_search_results(self, search_term):

        data = []

        search_url = f'{self.base_url}/topic/{search_term}'

        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(self.base_url, a['href']) for a in soup.find_all('a', href=True) if self.allowed_domain in urljoin(self.base_url, a['href'])]
            filtered_links = self.filter_urls_by_keywords(links, search_term)
            print(f"Found {len(filtered_links)} links after filtering.")

            for idx, link in enumerate(filtered_links):
                if idx >= 5:
                    break
                time.sleep(2)
                link_response = requests.get(link)

                if link_response.status_code == 200:
                    link_soup = BeautifulSoup(link_response.text, 'html.parser')
                    link_text = link_soup.get_text(separator=' ', strip=True)
                    link_text = self.post_processing(link_text)
                    title_element = link_soup.find("title")
                    title = title_element.text.strip() if title_element else ''
                    date_element = link_soup.find('time')
                    date_text = ""
                    if date_element:
                        date_text = date_element.text.strip()
                    data.append({
                        "Title": title,
                        "URL": link,
                        "Date": date_text,
                        "Page Content": link_text
                    })

                    print(f"Content from {link} stored.")

                else:
                    data.append({
                        "Title": "Failed to fetch page content for {link}",
                        "URL": link,
                        "Date": date_text,
                        "Page Content": ""
                    })

            print("Complete!")

        else:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")

        df = pd.DataFrame(data)
        return df
    

   
    
search_term = input("Enter search term:")
scraper = EconomicTimesScraper()
df = scraper.fetch_search_results(search_term)
#print(df.head(2))


#df.to_csv(f"{search_term}_data.txt", index=False, header=False, sep="\t")
#print(f"Data saved to {search_term}_data.txt")
