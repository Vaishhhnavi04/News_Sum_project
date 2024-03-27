import streamlit as st
from langchain_community.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.mapreduce import MapReduceChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq

import os
import time
import re
import requests
import groq
from bs4 import BeautifulSoup

import chainlit as cl

GROQ_API_KEY = "gsk_C1eFzyTKBU7zmmAsJ3NaWGdyb3FYh12Ztvh6l1xS8DQgG9ya@L60"

async def answer_question_with_extracted_text(question, text):
    searcher = groq.Searcher(GROQ_API_KEY)
    response = searcher.query(text, question)

    if response.get("choices"):
        return response.get("choices")[0].get("message").get("content")

    return "I'm not sure how to answer your question."

@cl.on_chat_start
async def on_chat_start():
    await cl.message("Please provide a URL to get started.")

@cl.on_message
async def on_message(message):
    if not message.text:
        await cl.message("Please provide a valid URL or a question. If you want to provide a URL, enter the URL first.")

    url = message.text

    if re.match(r"https?://\S+", url):
        cl.stop()

        await cl.message("Text extraction started...")

        question = await answer_question_with_extracted_text(
            "Extract text from the webpage", url
        )

        while True:
            user_question = await cl.input("Question:")

            if not user_question.strip():
                continue

            response = await answer_question_with_extracted_text(user_question, question)
            await cl.message(response, role="assistant")

if __name__ == "__main__":
    cl.run(qa_url_bot.py)