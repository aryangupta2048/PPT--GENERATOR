# =========================== STEP 1 ==============================================
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

# ======================== STEP 2 : LOAD ENV AND API KEYS=============================
st.title("Your Agentic PPT Generator")
st.header("""User can generate PPT , Images and fetch latest news""")

st.sidebar.title("Give API keys")

google_api_key = st.sidebar.text_input("google_api_key",type = "password")
tavily_api_key = st.sidebar.text_input("tavily_api_key",type = "password")

all_api = [google_api_key , tavily_api_key]

if not all(all_api):
  st.sidebar.error (" Must pass all api keys")
  
  url = "https://aistudio.google.com/app/api-keys"
  st.markdown(f"Get Google API key-{url}")

  url = "https://app.tavily.com/playground"
  st.markdown(f"Get Tavily API key-{url}")

elif all (all_api):
  st.success("API KEYS LOADED")
  options = ["gemini-3.5-flash-lite","gemini-3.5-flash",
            "
