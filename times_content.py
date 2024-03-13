import requests
from bs4 import BeautifulSoup
import re

def scrape(search_term):
    base_url="https://timesofindia.indiatimes.com"
    search_url=base_url+f"/topic/{search_term}"

    response= requests.get(search_url)
    if response.status_code == 200:
        soup=BeautifulSoup(response.content,"html.parser")

        search_results = soup.find_all("div", class_="uwU81")

        with open(f"{search_term}_search_results.txt","w", encoding="utf-8") as file:
            for result in search_results:
                title = result.find("span").text.strip()
                url = result.find("a")["href"].strip()
                published_date=result.find_all("div", class_="ZxBIG")[0].text.strip()
                file.write(f"Title:{title}\n")
                file.write(f"URL:{url}\n")
                file.write(f"Date:{published_date}\n")

                # Extract page content
                response= requests.get(url)
                if response.status_code == 200:
                    soup=BeautifulSoup(response.content,"html.parser")
                    content = soup.find("div", class_="_s30J clearfix").get_text()
                    content = re.sub(r'\s+', ' ', content).strip()
                    file.write(f"Page Content:{content}\n")
                    file.write("\n")
                else:
                    file.write(f"Failed to fetch page content for {url}\n")
                    file.write("\n")

        print("Data saved to file")
    else:
        print("failed to fetch search results")

search_term=input("Entersearch term:")
scrape(search_term)