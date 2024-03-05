import os
from bs4 import BeautifulSoup
import requests
import json
from newsapi import NewsApiClient
from openai import OpenAI
from flask import Flask, render_template

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

API_KEY_NEWSAPI = os.environ.get("news_api")
API_KEY_OPENAI = os.environ.get("open_ai_api")
'''url = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={API_KEY_NEWSAPI}"

response = requests.get(url)

if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)'''


@app.route('/')
def display_articles():
    url = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={API_KEY_NEWSAPI}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        articles = []
        for article in data['articles']:
            # Fetch the full article using the article's URL
            article_response = requests.get(article['url'])

            if article_response.status_code == 200:
                soup = BeautifulSoup(article_response.text, 'html.parser')
                article_content_div = soup.find('div', {'class': 'article-content'})
                article_content = ''
                for p_tag in article_content_div.find_all('p'):
                    article_content += p_tag.get_text()

                # Summarize the article content
                client = OpenAI(api_key=API_KEY_OPENAI)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        # recheck type of summarization.
                        {"role": "system", "content": "You are a helpful news assistant that summarizes news articles."},
                        {"role": "user", "content": f"Summarize the following article in 150 words: {article_content}"}
                    ],
                    temperature=0.7,
                    max_tokens=100
                )
                article_summary = response.choices[0].message.content.strip()

                # Simplify the article content
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful news assistant that explains news articles in simple language."},
                        {"role": "user", "content": f"Explain the following news article content: {article_content} in a way that is easy to understand for anyone, even someone without any specific knowledge of the subject. Please avoid using technical jargon and simplify any complex concepts. It is important that your explanation is based solely on the information in the article and does not include any fabricated information. Additionally, please explain any abbreviations used in the article so that someone unfamiliar with them can understand the full context."}
                    ],
                    temperature=0,
                    max_tokens=200
                )
                simplified_article = response.choices[0].message.content.strip()

                articles.append({
                'title': article['title'],
                'url': article['url'],
                'summary': article_summary,
                'simplified_article': simplified_article
        })

    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)