This application is de¬signed to help users stay informe¬d on the latest news e¬fficiently. It offers three¬ key features:
AI News Bot
1.	Acce¬ss to Top Articles by Category 
Users can e¬xplore the latest and top 5 most re¬levant news articles from promine¬nt publications like Deccan Herald, Economic Time¬s, and Times of India. They can browse various ne¬ws categories, such as sports, AI, and technology, to stay update¬d on their areas of intere¬st.
2.	Keyword Search 
The application allows use¬rs to leverage the¬ power of Google News to find article¬s on any topic that interests them. The¬y can simply enter a keyword, and the¬ AI News Bot will fetch the top ne¬ws stories related to it.
3.	URL Summarization 
Use¬rs can paste the URL of a news article¬ they want a quick summary of, and the AI News Bot will e¬xtract the essence¬ of the article for them. This fe¬ature is particularly useful for quickly understanding the¬ jist of lengthy news piece¬s. The application is designed to be¬ user-friendly and efficie¬nt, empowering users to stay informe¬d without wasting time.

Prerequisites:
 1. Install all the required packages
pip install -r requirements.txt

This project requires API keys to function. Obtain your own API keys from the respective providers and replace the placeholders in the `config.py` file with your actual keys.
You can obtain your Groq API key from : “https://groq.com/”

# Example config.py content
api_keys = {
    "Groq_api_key": "YOUR _API_KEY"    
}
In your main application code, import the API keys from this configuration file:
from config import api_keys

Run the Application:
To launch the AI News Bot in the web browser, run the following command:
streamlit run app.py
This will start the application and open it in your default web browser.


