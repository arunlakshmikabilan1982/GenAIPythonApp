import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from Navigation import sidebar

sidebar()
 
load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key) 

# st.set_page_config(page_title="Language Translator", page_icon="🌐")
st.header("Interactive Language Translation Tool")
 
# model = genai.GenerativeModel('gemini-pro')

def translate_text(source_language, target_language, text):
    language_codes = {
        "English": "en",
        "Chinese": "ch",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Arabic": "ar",
    }
    source_code = language_codes[source_language]
    target_code = language_codes[target_language]

    with st.spinner("Translating..."):
        response = client.models.generate_content(model="gemini-2.0-flash", contents =f"Translate the following sentence from language code {source_code} to {target_code}: {text}")
    
    return response.text

text = st.text_area("Please input the text you'd like to translate:")
source_language = st.selectbox("Source Language", ["English", "French", "Spanish", "German", "Arabic","Chinese"])
target_language = st.selectbox("Target Language", ["French", "Chinese", "Arabic", "Spanish", "German","English"])

if st.button("Translate"):
    if text:
        translated_text = translate_text(source_language, target_language, text)
        # Display translated text
        st.write(f"Translation: {translated_text}")
    else:
        st.warning("Please input the text you'd like to translate:")
