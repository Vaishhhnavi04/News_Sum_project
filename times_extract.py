import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class TOIScraper:
    def __init__(self):
        self.base_url = 'https://timesofindia.indiatimes.com/'
        self.url_keywords = [
            'technology', 'tech', 'ai', 'artificial-intelligence', 'machine-learning',
            'data-science', 'innovation', 'startup', 'sports', 'marketing', 'science'
        ]
        self.exclude_segments = [ '/prime/', '/entertainment/', '/nation']
        self.allowed_domain = "timesofindia.indiatimes.com"

    def filter_urls_by_keyword(self, link):

        if self.allowed_domain not in link:
            return None
        if not any(keyword in link for keyword in self.url_keywords):
            return None
        if any(segment in link for segment in self.exclude_segments):
            return None
        else:
            return link

    def scrape(self, search_term):
        search_url = self.base_url + f"/topic/{search_term}"

        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            search_results = soup.find_all("div", class_="uwU81")

            data = []
            for result in search_results:
                title = result.find("span").text.strip()
                url = result.find("a")["href"].strip()
                filtered_url = self.filter_urls_by_keyword(url)
                if filtered_url:
                    response = requests.get(filtered_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        content = soup.find("div", class_="_s30J clearfix").get_text()
                        content = re.sub(r'\s+', ' ', content).strip()
                        published_date = result.find_all("div", class_="ZxBIG")[0].text.strip()

                        data.append({
                            "Title": title,
                            "URL": url,
                            "Date": published_date,
                            "Page Content": content
                        })
                    else:
                        data.append({
                            "Title": title,
                            "URL": url,
                            "Date": published_date,
                            "Page Content": f"Failed to fetch page content for {url}"
                        })
                else:
                    data.append({
                        "Title": title,
                        "URL": url,
                        "Date": published_date,
                        "Page Content": f"Failed to fetch page content for {url}"
                    })

            df = pd.DataFrame(data)
            return df
        else:
            print("failed to fetch search results")
            return pd.DataFrame()

search_term = input("Enter search term:")
scraper = TOIScraper()
df = scraper.scrape(search_term)
#print(df.head(3))