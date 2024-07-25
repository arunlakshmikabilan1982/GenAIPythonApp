from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from langchain import PromptTemplate
from Navigation import sidebar

sidebar()

# Load environment variables (if necessary)
# load_dotenv()

# Load API key securely from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Set Streamlit page configuration
# st.set_page_config(page_title="Description of Products", page_icon="📸")

# Define prompt template for image description
prompt_template: str = """/
    Provide a detailed technical description and brief explanation of the object in the image.And
    Provide a detailed technical explanation, specifications, and information on different varieties of the object in the image.
    Describe the object's key features, materials, dimensions, and functionalities visible in the image.
    Discuss the various types or models available and identify which variety is the most sold or popular in the market.
"""
prompt = PromptTemplate.from_template(template=prompt_template)

# Function to get Gemini AI response based on image and prompt
def get_gemini_response(prompt_formatted_str, image):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    if prompt_formatted_str != "":
        response = model.generate_content([prompt_formatted_str, image])
    else:
        response = model.generate_content(image)
    return response.text

# Streamlit UI
st.header("Image to Text Description")

# Placeholder input for initial prompt
input_prompt = "describe the object"
prompt_formatted_str: str = prompt.format(question=input_prompt)

# File upload section for image
uploaded_file = st.file_uploader("Please select the image you would like to upload.", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to trigger description generation
if st.button("Describe object in the image"):
    if image is not None:
        # Display loading spinner while generating response
        with st.spinner("Generating description..."):
            response = get_gemini_response(prompt_formatted_str, image)
        # Display response
        st.subheader("Product Description")
        st.write(response)
    else:
        st.warning("Before proceeding, please upload an image.")
