import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv
from langchain import PromptTemplate
 
load_dotenv()  # take environment variables from .env.
api_key = os.getenv("GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key=api_key)
 
st.set_page_config(page_title="Chatbot", page_icon="🤖")
 
st.header("ChatBot - Ask me anything")
 
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
 
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
 
prompt_template: str = """/
Use the following pieces of context to answer the question/
question: {question}.
say Thank you....! at the end/
"""
 
prompt = PromptTemplate.from_template(template=prompt_template)
 
def askgenaibot(input):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
    response = model.generate_content(f"Generate Content {input}")
    return response.text

input = st.text_input("Input Prompt: ",key="input")
prompt_formatted_str: str = prompt.format(question=input)
if st.button("search"):
    response=askgenaibot(prompt_formatted_str)
    st.subheader("The Response is")
    st.write(response)
 
 