from bs4 import BeautifulSoup
import requests

def get_content(url):
    if not url.startswith("http"):
        url = "https://economictimes.indiatimes.com" + url

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_tag = soup.find('article')
        if article_tag is not None:
            text_content = article_tag.get_text()
            return text_content
        else:
            print("Failed to find the 'article' tag.")
            return ''
    else:
        print(f'Failed to fetch the URL. Status code: {response.status_code}')
        return ''


def scrape_articles(keywords):
    base_url = "https://economictimes.indiatimes.com"
    url_pattern =base_url+f"/topic/{keywords}" #"https://economictimes.indiatimes.com/topic/sports"

    response = requests.get(url_pattern)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        article_elements = soup.find_all("div", class_="contentD")

        with open(f"{keywords}_scrap_file_eco.txt", mode="w", encoding="utf-8") as txtfile:
            for article_element in article_elements:
                title_element = article_element.find("h2")
                if title_element is not None:
                    title = title_element.text.strip()
                    url = base_url + article_element.find("a")["href"]
                    if not url.startswith("http"):
                        url = base_url + url

                    txtfile.write(f"Title: {title}\nURL: {url}\n\n")
                    i=0
                    text_content = get_content(url)
                    if text_content is None:
                        print("text unavailable")
                    txtfile.write(text_content)
                    txtfile.write("\n---\n")

keywords=input("Enter search term:")
scrape_articles(keywords)