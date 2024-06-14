from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from langchain import PromptTemplate
 
# load_dotenv()  
 
# api_key = os.getenv("GEMINI_API_KEY")
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
 
st.set_page_config(page_title="Description of Products", page_icon="📸")
 
prompt_template: str = """/
Use the following pieces of context to answer the question/
question: {question}. Do not answer any question which is not related to that image/
Describe the object in the image in detail, market price, focusing on the objects, scene, colors, and composition/
detailed information of how to use, how it is manufactured and history of it/
question is not related to image then
say Thank you....! at the end/
"""
 
prompt = PromptTemplate.from_template(template=prompt_template)
 
def get_gemini_response(prompt_formatted_str,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if prompt_formatted_str!="":
       response = model.generate_content([prompt_formatted_str,image])
    else:
       response = model.generate_content(image)
    return response.text
 
st.header("Image to Text Descripton")
# input = st.text_input("Input Prompt: ",key="input")
input = "describe the object"
prompt_formatted_str: str = prompt.format(
    question=input)
 
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""  
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True, )
submit=st.button("Describe object in the image")
 
if submit:    
    response=get_gemini_response(prompt_formatted_str,image)
    st.subheader("Product Description")
    st.write(response)