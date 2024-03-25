import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from summarize_with_llm import LLM_Summarizer



llm = LLM_Summarizer()
st.title("URL Summarizer")
url_input =st.text_area("Enter URL(s) for summarization (one per line)")
if url_input:
        urls=url_input.split("\n")
        for url in urls:
                llm=ChatGroq(temperature=0,
                            model_name="mixtral-8x7b-32768",
                            api_key="gsk_C1eFzyTKBU7zmmAsJ3NaWGdyb3FYh12Ztvh6l1xS8DQgG9ya@L60")

        system="You are an expert summarizer of text content in URL links" 
                #human= "{text]"
        human = "Summarize the news content in five sentences."

        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain=prompt | llm

        response=chain.invoke({"text": "Summarize the news content in five sentences" + url}) 
        st.write(response.content)
        st.write(url)
                