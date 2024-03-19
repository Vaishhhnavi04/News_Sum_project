import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

class DeccanScrapper:
    def __init__(self):
        self.base_url = "https://www.deccanchronicle.com"
        self.url_keywords = [
            'technology', 'tech', 'ai', 'artificial-intelligence', 'machine-learning',
            'data-science', 'innovation', 'startup', 'sports', 'marketing', 'science'
        ]
        self.exclude_segments = ['/news/', '/prime/', '/entertainment/', '/nation']
        self.allowed_domain = "deccanchronicle.com"

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
        data = []
        base_url = "https://www.deccanchronicle.com"
        search_url = base_url + f"/search?search={search_term}"

        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("div", class_="col-lg-3 col-sm-6 grid-margin mb-5 mb-sm-2")
            count=0
            for result in articles:
                if count >= 5:
                    break
                title = result.find("h5", class_="font-weight-bold mt-3 grid-heading").text.strip()
                url = result.find("a")["href"]
                if not url.startswith("http"):
                    url = "https://www.deccanchronicle.com" + url
                published_date = result.find("span", class_="date convert-to-localtime").text.strip()

                filtered_url = self.filter_urls_by_keyword(url)
                if filtered_url:
                    response = requests.get(filtered_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        additional_content1 = soup.find("div", class_="col-md-12 col-sm-12").get_text()
                        content = soup.find_all('div', {'class': 'story_content details-story-wrapper details-content-story article_cont_size'})
                        if content:
                            content_text = content[0].get_text()
                            # Concatenate all the content
                            content_text = additional_content1 + content_text
                            data.append({
                                "Title": title,
                                "URL": filtered_url,
                                "Date": published_date,
                                "Page Content": content_text
                            })
                        else:
                            data.append({
                                "Title": title,
                                "URL": filtered_url,
                                "Date": published_date,
                                "Page Content": "No content found"
                            })
                    else:
                        data.append({
                            "Title": title,
                            "URL": filtered_url,
                            "Date": published_date,
                            "Page Content": f"Failed to fetch page content for {filtered_url}"
                        })
                    
                    count += 1
                else:
                    continue

            df = pd.DataFrame(data)
            print("Data saved to DataFrame")
            return df
        else:
            print("failed to fetch search results")

search_term = input("Enter search term:")
scraper = DeccanScrapper()
df = scraper.scrape(search_term)
print(df)
