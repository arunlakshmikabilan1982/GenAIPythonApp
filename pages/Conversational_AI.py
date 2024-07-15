import os
import streamlit as st
from dotenv import load_dotenv
from langchain import PromptTemplate
import google.generativeai as genai
from Navigation import sidebar

sidebar()

# Load environment variables
load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"]

# Configure Generative AI model and API
model = genai.GenerativeModel(model_name='gemini-pro')
genai.configure(api_key=api_key)

# Configure Streamlit page
# st.set_page_config(page_title="Conversational AI", page_icon="🤖")

# Header and initial setup
st.header("Conversational AI")

# Generation configuration and safety settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Prompt template for generating responses
prompt_template = """
Generate a response based on the following query:
query: {query}.
"""

prompt = PromptTemplate.from_template(template=prompt_template)

# Function to interact with the generative AI model
def ask_genai_bot(input_prompt):
    response = model.generate_content(input_prompt)
    return response.text

# Streamlit UI components
input_prompt = st.text_area("Please enter your query below.", key="query_input")
# input_prompt = st.text_input("Input Prompt: ", key="input")
prompt_formatted_str = prompt.format(query=input_prompt)

if st.button("Generate response"):
    # Display loading spinner while generating response
    with st.spinner("Generating response..."):
        try:
            response = ask_genai_bot(prompt_formatted_str)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
