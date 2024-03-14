import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def filter_urls_by_keyword(link, keywords, allowed_domain,exclude_segments):

        if allowed_domain not in link:
            return None
        if not any(keyword in link for keyword in keywords):
            return None
        if any(segment in link for segment in exclude_segments ):
            return None
        else:
            return link

def scrape(search_term):
    base_url = "https://www.deccanchronicle.com"
    search_url = base_url + f"/search?search={search_term}"

    url_keywords = [
        'technology', 'tech', 'ai', 'artificial-intelligence', 'machine-learning',
        'data-science', 'innovation', 'startup', 'sports', 'marketing'
    ]
    exclude_segments = ['/news/', '/prime/', '/stocks/', '/entertainment/']

    allowed_domain = "deccanchronicle.com"

    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="col-lg-3 col-sm-6 grid-margin mb-5 mb-sm-2")

        with open(f"{search_term}_filtered_results_deccan.txt", "w", encoding="utf-8") as file:
            for result in articles:
                title = result.find("h5", class_="font-weight-bold mt-3 grid-heading").text.strip()
                url = result.find("a")["href"]
                if not url.startswith("http"):
                    url = "https://www.deccanchronicle.com" + url
                published_date = result.find("span", class_="date convert-to-localtime").text.strip()

                filtered_url = filter_urls_by_keyword(url, url_keywords, allowed_domain, exclude_segments)
                if filtered_url:
                    file.write(f"Title:{title}\n")
                    file.write(f"URL:{filtered_url}\n")
                    file.write(f"Date:{published_date}\n")

                    response = requests.get(filtered_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        # Extract additional content
                        additional_content1 = soup.find("div", class_="col-md-12 col-sm-12").get_text()
                        content = soup.find_all('div', {'class': 'story_content details-story-wrapper details-content-story article_cont_size'})
                        if content:
                            content_text = content[0].get_text()
                            # Concatenate all the content
                            content_text = additional_content1 + "\n" + content_text
                            file.write(f"Page Content:{content_text}\n")
                            file.write("\n")
                    else:
                        file.write(f"Failed to fetch page content for {filtered_url}\n")
                        file.write("\n")
                else:
                    continue

        print("Data saved to file")
    else:
        print("failed to fetch search results")

search_term = input("Enter search term:")
scrape(search_term)