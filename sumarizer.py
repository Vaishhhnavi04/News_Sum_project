import os
import re
import pandas as pd
import streamlit as st
import nltk
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import AzureChatOpenAI
from langchain.docstore.document import Document

nltk.download("punkt")
from nltk.tokenize import word_tokenize

import os
import re
import pandas as pd
import streamlit as st
import nltk
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import AzureChatOpenAI
from langchain.docstore.document import Document

nltk.download("punkt")
from nltk.tokenize import word_tokenize

AZURE_BASE_URL = "https://openai-lh.openai.azure.com/openai"
AZURE_OPENAI_API_KEY = "fb3a0027e2c64a52adae3ba9f4b67583"

llm = AzureChatOpenAI(
    azure_endpoint="https://openai-lh.openai.azure.com/openai",
    azure_deployment="LH-GPT",
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-03-15-preview",
    openai_api_type="azure",
    temperature=0.0,
    frequency_penalty=0.5,
    presence_penalty=0.5
)

def break_up_file(tokens, chunk_size, overlap_size):
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(tokens[chunk_size - overlap_size:], chunk_size, overlap_size)

def break_up_file_to_chunks(stringname, chunk_size=6000, overlap_size=0):
     tokens = word_tokenize(stringname)
     return list(break_up_file(tokens,chunk_size,overlap_size))

def convert_to_detokenized_text(tokenized_text):
    prompt_text=" ".join(tokenized_text)
    prompt_text = prompt_text.replace(" 's", "'s")
    return prompt_text

def summarize_text(text):
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    result = chain({"input_documents": [Document(page_content=text.strip())]})
    summary = result["output_documents"][0].page_content
    print(summary)
    return summary


def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    text_content = []
    for i, row in df.iterrows():
        url = row["URL"]
        page_content = row["Page Content"]
        text_content.append((url, page_content))
    return text_content

st.title("Al newspaper Summarizer")

text_content = load_csv_file(r'F:\pythonprojects\newsapppython\sports_filtered_results_deccan.csv')
#print(text_content)

summaries = []
urls = []
for url, page_content in text_content:
            print("loop")
            print(page_content)
            summary = summarize_text(page_content)
            summaries.append(summary)
            urls.append(url) 


'''if st.button("Summarize"):
    if text_content is not None:
        st.success("Loaded scrapped text")
        summaries = []
        urls = []
        for url, page_content in text_content:
            print("loop")
            print(page_content)
            summary = summarize_text(page_content)
            summaries.append(summary)
            urls.append(url) 
        df = pd.DataFrame(list(zip(urls, summaries)), columns=["URL", "Summary"])
        st.write(df)'''