import streamlit as st
#from langchain.agents.react.base import Docstoreexplorer

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#from streamlit_extras.switch_page_button import switch_page


import streamlit as st
from pages import url_page
from langchain_community.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.mapreduce import MapReduceChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from deccan_extract import DeccanScrapper
from times_extract import TimesofIndiaScrapper
from ecotimes_filtered import EconomicTimesScraper
from googlenews_extract import Googlescrapper
from summarize_with_llm import LLM_Summarizer
#from url_page import urlsum
import importlib


import pandas as pd
import os
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq



from pages import url_page
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
#from utils.economic_times_extract import EconomicTimesScrapper
#from utils.deccan_extract import DeccanScrapper
#from utils.times_of_india_extract import TimesofIndiaScrapper
#from utils.extract_using_google import Googlescrapper
#from utils.summarize_using_llm import LLM_summarizer



st.title("AI Newspaper Summarizer")
newspapers = ["ET", "Deccan_Herald", "TOI","google","URL"]
user_search = st.text_input('Enter your search term:')

st.sidebar.title("select a newspaper")
selected_newspaper=st.sidebar.radio("",newspapers)

search_mapper={
    'ai':'ET',
    'finance':'TOI',
    'sports':'TOI',
    'technology':'ET',
    'marketing':'TOI',
}



default_index = 0

if user_search:
    for keyword, newspaper in search_mapper.items():
        if keyword in user_search.lower():
            default_index = newspapers.index(newspaper)
            break

    st.session_state.radio_key += 1
    selected_newspaper = st.sidebar.radio("", newspapers, index=default_index, key=f"newspaper_key_{st.session_state.radio_key}")


llm = LLM_Summarizer()



if st.sidebar.button("Submit"):
  
    if user_search:
        for keyword, newspaper in search_mapper.items():
            if keyword in user_search.lower():
                selected_search = newspaper
                break
        else:
            selected_search = selected_newspaper


if selected_newspaper == "URL":
        st.switch_page("pages/url_page.py")
        
        

elif selected_newspaper=="ET" and user_search:
    scraper=EconomicTimesScraper()
    data=scraper.fetch_search_results(user_search)
    st.success("Loaded scrapped data for Economic times")
    summary=llm.summarize_text(data)
    st.write(summary)

elif selected_newspaper=="Deccan_herald" and user_search:
    scraper=DeccanScrapper()
    data=scraper.scrape(user_search)
    st.success("Loaded scrapped data for Deccan times")
    summary=llm.summarize_text(data)
    st.write(summary)

elif selected_newspaper=="TOI" and user_search:
    scraper=TimesofIndiaScrapper()
    data=scraper.scrape(user_search)
    st.success("Loaded scrapped data")
    summary=llm.summarize_text(data)
    st.write(summary)

elif selected_newspaper=="Google" and user_search:
    scraper=Googlescrapper()
    #data=scraper.scrape(user_search)
    st.success("Loaded scrapped data")
    summary=scraper.scrape(user_search)
    st.write(summary)


else:
        pass