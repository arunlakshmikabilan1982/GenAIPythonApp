import os
import streamlit as st
import google.generativeai as genai
from environment import GEMINI_API_KEY

# Configure the Generative AI API
genai.configure(api_key=GEMINI_API_KEY)

# Create the GenerativeModel instance
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Streamlit app
def main():
    st.title("AI Translator")

    # Input fields for source language, target language, and text
    sourcelanguage = st.text_input("Enter source language:")
    targetlanguage = st.text_input("Enter target language:")
    text = st.text_area("Enter text to translate:")

    # Translate button
    if st.button("Translate"):
        if sourcelanguage.strip() == '' or targetlanguage.strip() == '' or text.strip() == '':
            st.error("Please fill in all fields.")
        else:
            # Generate translation
            response = model.generate_content(f"Translate the following sentence from language {sourcelanguage} to language {targetlanguage}: {text}")
            translated_text = response.text

            # Display translated text
            st.success(f"Translated text: {translated_text}")

if __name__ == "__main__":
    main()
