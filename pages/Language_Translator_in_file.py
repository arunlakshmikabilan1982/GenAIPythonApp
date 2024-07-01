import os
import google.generativeai as genai
import streamlit as st
from io import BytesIO
import docx
from fpdf import FPDF

from Navigation import sidebar

sidebar()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# st.set_page_config(page_title="File Translator", page_icon="📄")
st.header("File Translator 🌐")

model = genai.GenerativeModel('gemini-pro')

def translate_text(text, source_lang, target_lang):
    response = model.generate_content(f"Translate the following sentence from {source_lang} to {target_lang}: {text}")
    return response.text

def translate_file_in_docx(file, source_lang, target_lang, file_name):
    doc = docx.Document(BytesIO(file.read()))
    document = docx.Document()
    fpdf = FPDF()
    fpdf.add_page()
    for para in doc.paragraphs:
        text = para.text
        if text:
            # st.write(text)
            translated_text = translate_text(text, source_lang, target_lang)
            # st.write(translated_text)                
            document.add_paragraph(translated_text)
            document.save(f'Downloads/{file_name}')                 
    print('Data has been written to example.docx')

def translate_file_in_pdf(file, source_lang, target_lang, file_name):
    doc = docx.Document(BytesIO(file.read()))
    fpdf = FPDF()
    fpdf.add_page()
    for para in doc.paragraphs:
        text = para.text
        if text:
            st.write(text)
            translated_text = translate_text(text, source_lang, target_lang)
            st.write(translated_text)                    
            fpdf.set_font("Arial", size=25)
            fpdf.text(50, 50, txt= translated_text) 
            fpdf.output(f"Translated_{file_name}.pdf")                     
    print('Data has been written to example.docx')

def main():
    uploaded_file = st.file_uploader("Upload a file (.txt, .docx)", type=['txt', 'docx'])
    if uploaded_file is not None:
        source_language = st.selectbox("Select Source Language", ["English", "French", "Spanish", "German", "Arabic"])
        target_language = st.selectbox("Select Target Language", ["French", "Chinese", "Arabic", "Spanish", "German"])

        docx_btn, pdf_btn = st.columns([1,1])
        with docx_btn:
            if st.button("Translate in docx"):
                translate_file_in_docx(uploaded_file, source_language.lower(), target_language.lower(), uploaded_file.name)
        with pdf_btn:
            if st.button("Translate in pdf"):
                translate_file_in_pdf(uploaded_file, source_language.lower(), target_language.lower(), uploaded_file.name)
        # if st.button("Translate as docx"):
        #     translate_file_in_docx(uploaded_file, source_language.lower(), target_language.lower(), uploaded_file.name)
        # elif st.button("Translate as pdf"):
        #     translate_file_in_pdf(uploaded_file, source_language.lower(), target_language.lower(), uploaded_file.name)


if __name__ == "__main__":
    main()
