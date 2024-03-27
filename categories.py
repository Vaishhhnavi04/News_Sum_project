import requests
import time
from bs4 import BeautifulSoup

def categories_deccan():
    print("Scarpping deccan data")
    url = 'https://www.deccanchronicle.com/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    menu = soup.find('ul', {'id': 'menu-main-hmenu'})

    categories = []
    for item in menu.find_all('li'):
        # Get the text of the menu-name span
        name = item.find('span', class_= 'menu-name')
        if name is not None:
            categories.append(name.text.strip())

    print(categories)
    #print(len(categories))
    return categories

def categories_et():

    print("\n\nScarpping ecotimes data \n")
    url = 'https://economictimes.indiatimes.com/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    nav_element = soup.find('nav', {'class': 'level1'})

    subcategories = [item.get_text() for item in nav_element.find_all('div', {'data-ga-action': True})]
    
    #print(", ".join(subcategories))
    print(subcategories)
    return subcategories




def categories_times():

    print("\n\nScarpping times data \n")
    url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories_ul = soup.find('ul', {'itemtype': 'http://www.schema.org/SiteNavigationElement'})

    # If the ul element is found
    if categories_ul:
        categories = [li.find('a').text.strip() for li in categories_ul.find_all('li')]
        print(categories)
        return categories
       
    else:
        return []
    

categories_deccan()
categories_et()
categories_times()


