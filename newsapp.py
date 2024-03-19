import subprocess
import sys
import streamlit as st
from langchain.agents.react.base import DocstoreExplorer
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI

from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

# Import necessary libraries
from deccan_extract import DeccanScrapper

import openai
import platform
import os
import pandas as pd

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

AZURE_BASE_URL = "https://openai-lh.openai.azure.com/openai"
AZURE_OPENAI_API_KEY = "312ff50d6d954023b8748232617327b6"

llm1 = AzureChatOpenAI(
    openai_api_base=AZURE_BASE_URL,
    openai_api_version="2023-06-01-preview",
    deployment_name="LH-GPT",
    openai_api_key=AZURE_OPENAI_API_KEY,
    openai_api_type="azure",
    temperature=0.0,
    max_tokens=200,
    # top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    verbose=True
    
)

llm2 = AzureChatOpenAI(
    openai_api_base=AZURE_BASE_URL,
    openai_api_version="2023-06-01-preview",
    deployment_name="LH-GPT",
    openai_api_key=AZURE_OPENAI_API_KEY,
    openai_api_type="azure",
    temperature=0.0,
    max_tokens=500,
    # top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    verbose=True
    
)


def summarize_text(file_path):

    df=pd.read_csv(file_path)
    top_rows=df.head(5)
    summaries=[]
    urls=[]
    dates=[]

    for idx,row in top_rows.iterrows():
        url=row["URL"]
        date=row["Date"]
        url_content=row["Page Content"]
        prompt_request="Summarize this news content in three sentences: \n\n"+url_content,
        response=llm1.invoke(prompt_request)
        print(response.content)
        summaries.append(response.content)
        urls.append(url)
        dates.append(date)

    combined_text="\n\n".join(summaries)


    prompt="""Write a concise summary in bullet points along with keywords:
    step 1 : Summary
    Step 2 : Extracted Keywords of the content for which summary generated in step 1
    
    the below is how the output must look like:
    OUTPUT:
    concise summary:
    
    ________________________

    EXTRACTION of keywords:
    Extract the important keywords from the summary and categorize them in the format.
    Category: Extracted keywords
    
    Example:
    Company: Amazon, OpenAI
    Languages: Javascript, SQL
    
    """+ combined_text
    
    final_response=llm2.invoke(prompt)
    summary_list = []
    for i in range(len(summaries)):
        summary_dict = {
            "Summary": summaries[i],
            "URL": urls[i],
            "Date": dates[i]
        }
        summary_list.append(summary_dict)
    return final_response.content, summary_list
    
    #return final_response.content

st.title("AI Newspaper Summarizer")
newspapers = ["ET", "Deccan_Herald", "TOI"]
user_search = st.text_input('Enter your search term:')

st.sidebar.title("select a newspaper")
selected_newspaper=st.sidebar.radio("",newspapers)


text_content = None

if selected_newspaper=="ET" and user_search:
    scraper=DeccanScrapper()
    data=scraper.fetch_search_results(user_search)
    st.success("Loaded scrapped data for Economic times")
    final_response, summary_list = summarize_text(data)
    st.write(final_response)
    summary_df = pd.DataFrame(summary_list)
    st.write(summary_df)

elif selected_newspaper=="Deccan_herald" and user_search:
    scraper=DeccanScrapper()
    data=scraper.scrape(user_search)
    st.success("Loaded scrapped data for Deccan times")
    final_response, summary_list = summarize_text(data)
    st.write(final_response)
    summary_df = pd.DataFrame(summary_list)
    st.write(summary_df)
else:
    st.warning('')