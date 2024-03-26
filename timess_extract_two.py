import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class TimesofIndiaScrapper:
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
            count=0
            for result in search_results:
                if count >= 5:
                    break
                title = result.find("span").text.strip()
                url = result.find("a")["href"].strip()
                #print(url)
                
                filtered_url = self.filter_urls_by_keyword(url)
                print(filtered_url)
                published_date=""
                if filtered_url is not None:
                    response = requests.get(filtered_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        content = soup.find("div", class_="_s30J clearfix").get_text()
                        content = re.sub(r'\s+', ' ', content).strip()
                        published_date = result.find_all("div", class_="ZxBIG")[0].text.strip()
                        date_parts = published_date.split('/')[-1].strip().split(',')
                        published_date = ",".join(date_parts).strip()

                        data.append({
                            "Title": title,
                            "URL": filtered_url,
                            "Date": published_date,
                            "Page Content": content
                        })
                        count += 1
                    else:
                        continue
                        
                else:
                    continue

            df = pd.DataFrame(data)
            return df
        else:
            print("failed to fetch search results")
            return pd.DataFrame()

#search_term = input("Enter search term:")
#scraper = TimesofIndiaScrapper()
#df = scraper.scrape(search_term)
#print(df.head(2))

#df.to_csv(f"{search_term}_toidata.txt", index=False, header=False, sep="\n")


 