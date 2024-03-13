
import requests
from bs4 import BeautifulSoup
import re
def scrape(search_term):
    base_url="https://www.deccanchronicle.com"
    search_url=base_url+f"/search?search={search_term}" #https://www.deccanchronicle.com/search?search=sports

    response= requests.get(search_url)
    if response.status_code == 200:
        soup=BeautifulSoup(response.content,"html.parser")
        articles = soup.find_all("div", class_="col-lg-3 col-sm-6 grid-margin mb-5 mb-sm-2")

        with open(f"{search_term}_search_results_deccan.txt","w", encoding="utf-8") as file:
            for result in articles:
                title = result.find("h5", class_="font-weight-bold mt-3 grid-heading").text.strip()
                url = result.find("a")["href"]
                if not url.startswith("http"):
                    url = "https://www.deccanchronicle.com" + url
                published_date=result.find("span", class_="date convert-to-localtime").text.strip()
                file.write(f"Title:{title}\n")
                file.write(f"URL:{url}\n")
                file.write(f"Date:{published_date}\n")

                # Extract page content
                response= requests.get(url)
                if response.status_code == 200:
                    soup=BeautifulSoup(response.content,"html.parser")
                   # Extract additional content
                    
                    #additional_content1 = soup.find_all("div", class_="pb-4 pt-2 news-post-wrapper-sm").get_text()
                    additional_content1 = soup.find("div", class_="col-md-12 col-sm-12").get_text()
                    content = soup.find_all('div', {'class': 'story_content details-story-wrapper details-content-story article_cont_size'})
                    if content:
                        content_text = content[0].get_text()
                        # Concatenate all the content
                        content_text = additional_content1 +"\n" + content_text 
                        file.write(f"Page Content:{content_text}\n")
                        file.write("\n")
                else:
                    file.write(f"Failed to fetch page content for {url}\n")
                    file.write("\n")

        print("Data saved to file")
    else:
        print("failed to fetch search results")

search_term=input("Entersearch term:")
scrape(search_term)
