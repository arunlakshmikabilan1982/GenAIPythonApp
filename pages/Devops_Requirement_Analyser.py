import os, tempfile
import nest_asyncio
import google.generativeai as genai
from pathlib import Path
nest_asyncio.apply()
from langchain_core.prompts import PromptTemplate
import streamlit as st
from docx import Document
from fpdf import FPDF
from io import BytesIO
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from Navigation import sidebar

sidebar()

# api_key = st.secrets["GEMINI_API_KEY"]
from environment import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)
TMP_DIR = Path(__file__).resolve().parent.parent.joinpath('data', 'tmp')

# Configure Streamlit page
# st.set_page_config(page_title="Conversational AI", page_icon="🤖")

# Header and initial setup
st.header("DevOps Requirements Analyser")

st.session_state.uploaded_file = st.file_uploader("Please select the file you would like to upload",type=["pdf", "docx"])

def save_response_word_doc(response):
    worddoc = Document()
    worddoc.add_paragraph(response)
    worddoc_bytes = BytesIO()
    worddoc.save(worddoc_bytes)
    worddoc_bytes.seek(0)
    return worddoc_bytes
   
def save_response_pdf(response,filename): 
      fpdf = FPDF()
      fpdf.add_page()
      fpdf.set_font("Arial", size=10)
      fpdf.multi_cell(0, 10, txt=response.encode().decode('latin-1', 'strict'), align="L",)
      # fpdf.cell(200, 10, txt=response, align="C")
      newfilename = f"response-{filename}"
      tmp_location = os.path.join(TMP_DIR, newfilename)
      fpdf.output(tmp_location)
      return tmp_location, newfilename
def load_documents():
    if "uploaded_file" in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        if uploaded_file is not None:
            tmp_location = os.path.join(TMP_DIR, uploaded_file.name)
            file_extension = os.path.splitext(tmp_location)[1]
            with open(tmp_location, "wb") as file:
                file.write(uploaded_file.getvalue())

            if file_extension == ".pdf":
                loader = PyPDFLoader(tmp_location)
            elif file_extension == ".docx":
                loader = Docx2txtLoader(tmp_location)
            else:
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
                return None

            documents = loader.load()
            return documents
        else:
            st.warning("Please upload the file")
            return None


def process_docs(docs):
    prompt_template: str = r"""
          Generate DevOps Requirement details based on {content}, assuming AI role as {role}, Use below Template:
          Pre-Requisites: detailed list of pre-requisites needed to build the pipeline
          Requirements : Detailed list of requirements to build the Pipeline
          Considerations : Considerations, Notes for creating pipelines and setting up the CI/CD for the project
          Steps to create Build Pipeline: Mention the detailed steps to create the pipelines, and provide required azure devops scripts as an example
          Steps to create Release Pipeline: Mention the detailed steps to create the pipelines, and provide required azure devops scripts as an example

          role: {role}
          content: {content}
          """    
    prompt = PromptTemplate.from_template(template=prompt_template)
    role = "Requirements Analyser, DevOps Engineer, Have Knwoledge on DevOps"
    prompt_formatted_str: str = prompt.format(content = docs, role = role)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt_formatted_str)  
    return response.text

# input = st.text_input("Ask Me Query")

if st.button("Get Info"):
         documents = load_documents()
         if documents:
          with st.spinner("Generating info"):
            response = process_docs(documents)
          st.write(response)
          st.session_state.llmresponse = response

if "llmresponse" in st.session_state:
  uploaded_file = st.session_state.uploaded_file
  llmresponse = st.session_state.llmresponse
  tmp_location = os.path.join(TMP_DIR, uploaded_file.name)
  file_extension = os.path.splitext(tmp_location)[1]

  if file_extension == ".docx":
         output = save_response_word_doc(llmresponse)
         st.download_button(
                    label="Download the Response in DOCX",
                    data=output,
                    file_name=f"response_{uploaded_file.name}",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
         
  if file_extension == ".pdf":
         tmp_location, newfilename = save_response_pdf(llmresponse,uploaded_file.name)
         with open(tmp_location, "rb") as f:
            st.download_button(
                    label="Download the Response in PDF",
                    data=f,
                    file_name=newfilename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )      
