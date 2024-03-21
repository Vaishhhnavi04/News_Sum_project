# Import necessary libraries
from GoogleNews import GoogleNews
import pandas as pd
import requests
import newspaper
from fake_useragent import UserAgent
import re

# Define the keyword to search.
keyword = input("Enter the search:")

# Perform news scraping from Google and extract the result into Pandas dataframe.
googlenews = GoogleNews(lang='en', region='US', period='1d', encode='utf-8')
googlenews.clear()
googlenews.search(keyword)

# Top news from the 1st page of Google News
googlenews.get_page(1)
news_result = googlenews.result(sort=True)
news_data_df = pd.DataFrame.from_dict(news_result)

# Defining the agent
ua = UserAgent()
scraped_links = set()
news_data_with_text = []

# Counter to track the number of successfully scraped articles
scraped_count = 0

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

for index, headers in news_data_df.iterrows():
    if scraped_count >= 5:  # Limit to 5 articles
        break
    
    news_link = str(headers['link'])
    if news_link in scraped_links:
        continue
    
    try:
        # Parse the HTML content using newspaper
        article = newspaper.Article(news_link, user_agent=ua.chrome)
        article.download()
        article.parse()
        news_title = article.title
        news_text = article.text
        news_summary = article.summary
        
        # Increment the scraped count
        scraped_count += 1
        
        # Add the link to the set of scraped links
        scraped_links.add(news_link)
    except Exception as e:
        print(f'\nHTML Content Scraped Error for {news_link}, Skipped\n')
        continue
    
    news_media = str(headers['media'])
    news_update = str(headers['date'])
    news_timestamp = str(headers['datetime'])
    news_description = str(headers['desc'])
    
    news_data_with_text.append([news_title, news_media, news_update, news_timestamp, news_description, news_link, news_text])
    print('HTML Content Scraped')
    print([news_title, news_media, news_update, news_timestamp, news_description, news_link, news_text])

# Create DataFrame from the scraped data
news_data_with_text_df = pd.DataFrame(news_data_with_text, columns=['Title', 'Media', 'Update', 'Timestamp', 'Description', 'Link', 'Content'])

# Apply HTML tag removal to the 'Content' column
news_data_with_text_df['Content'] = news_data_with_text_df['Content'].apply(remove_html_tags)

# Display the DataFrame
print(news_data_with_text_df.head(5))

# news_data_with_text_df.to_csv('news_data.csv')  # Uncomment to save to CSV
