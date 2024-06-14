import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
 
load_dotenv()  
# api_key = os.getenv("GEMINI_API_KEY")

api_key = st.secrets["GEMINI_API_KEY"]
 
genai.configure(api_key=api_key)
 
st.set_page_config(page_title="Language Translator", page_icon="🌐")
st.header("Interactive Language Translation Tool")
 
model = genai.GenerativeModel('gemini-pro')
text = st.text_area("Enter text to translate:")
 
source_language = st.selectbox("Source Language", ["English", "French", "Spanish", "German"])
target_language = st.selectbox("Target Language", ["French", "chinese", "Arabic", "Spanish", "German"])
 
language_codes = {
    "English": "en",
    "chinese": "ch",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic":"ar",
}
 
if st.button("Translate"):
    if text:
        response = model.generate_content(f"Translate the following sentence from language code {language_codes[source_language]} to {language_codes[target_language]}: {text}")
        st.write(f"Translation: {response.text}")
    else:
        st.write("Please enter text to translate.")
 