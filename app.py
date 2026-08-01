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
            "gemini-2.5-flash-lite","gemini-2.5-flash"]

  selected_model = st.selectbox("select-model", options = options)

  model = ChatGoogleGenerativeAI(
    model = selected_model,
    google_api_key = google_api_key)

else:
  st.sidebar.info("Try valid API-keys")

#======================step 3 : backend ================================
# Search_latest_info using Tavily
def search_latest_info(query):
  """This function helps to give
  latest search using tavily
  based on given user query related research or contents"""

  client = TavilyClient(api_key = tavily_api_key)
  response = client.search(query)
  return response
  

def generate_image(img_prompt,slide_no = 1):
  """this function helps user to generate
  image using free api , with given
  img_prompt , with slide no"""

  url = f"https://image.pollinations.ai/{img_prompt}"
  
  import requests as r
  content = r.get(url).content
  with open (f"ai_image_(slide_no).jpeg","wb") as f:
    f.write(content)
  return url

def run_agent(leader_agent, query):
    prompt = f"""Based on Below given Query,
    your task is to call specific tool, first to
    promptify user prompt, than call image tool, or
    latest search if required.give slide dynamic, ui ux,
    with creative design, keep help of function to generate image
    based on given topic,
    Generate image using
    with number of slide asked, and use time sleep to hit image request on server
    and using file handling embed this in output html, use java script function
    give Final response output in HTML, no markdowns
    user query given below:
    """

    prompt = prompt + query

    # prompt = agent_prompt(prompt)

    response = leader_agent.invoke({
        'messages': [
            {
                'role': 'user',
                'content': prompt}]})

    code = response['messages'][-1].content[-1]['text']
    return code


# leader_agent creation
if all(all_api):
  leader_agent = create_agent(
    model=model,
    tools = [search_latest_info,
             #generate image
             ])
  leader_agent
else:
  st.info("Give Api-keys first to load agent")

#====================Step 4 : Streamlit Navbars======================

tab1,tab2,tab3 = st.tabs(["generate image",
                          "fetch news",
                          "generate ppt"])
user_input = st.text_area("write prompt & click enter")

if (user_input) & (leader_agent):
  with tab1:
    if st.button("Click to Generate Image"):
      with st.spinner("running agent"):
        try:
          url = generate_image(user_input)
          import requests as r
          img_data = r.get(url)
          st.image(url)
        except Exception as err:
          st.error("Error code:",err)

with tab2:
  if st.button("fetch latest news",key = "news-button"):
    with st.spinner("running agent")
      try:
        prompt = """give latest news related to given user query
        in dynamic html , output with card design format.
        Strict HTML Output, No Any markdowns Repsonse
        User Query: """ + user_input

        response = leader_agent.invoke({"messages": [{"role": "user",
                                                              "content": prompt}]})

        code = response["messages"][-1].content[-1]["text"]
        st.html(code,width="stretch",unsafe_allow_javascript=True)

      except Exception as err:
        st.error("Error Code:", err)

with tab3:
  if st.button("click to generate PPT",key="PPT-Button"):
    with st.spinner("running agent"):
      try:
        code = run_agent(leader_agent , user_input)
        st.html(code,width='stretch',unsafe_allow_javascript=True)

        if st.download_button(label = "DOWNLOAD PPT",
                              data = code,
                              file_name = 'ppt.html',
                              mime = 'text/html'):
            st.success("PPT downloaded successfully!!")

      except Exception as err:
        st.error("Error code:",err)
