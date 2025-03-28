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
TMP_DIR = Path(__file__).resolve().parent.joinpath('data', 'tmp')

# Configure Streamlit page
# st.set_page_config(page_title="Conversational AI", page_icon="🤖")

# Header and initial setup
st.header("Pre-Sale Analysis")

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
      newfilename = f"response-presale-{filename}"
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
          Generate asked details based on {content}, Use below Template strictly:

          Technical Requirements -- List of All the technical requirements mentioned, list should be bulleted
          Functional Requirements -- List of All the functional requirements mentioned, list should be bulleted 
          Performance Testing -- All the important details like configuration,features about the image, Not to exceed 50 words, should be in paragraph
          Hosting -- Mentioned Requirements on Hosting
          Timeline or Schedule -- Delivery timeline related information, Project Timeline, Schedule details
          Testing Scpe, QA -- Information related to Scope of Testing of the system or application
          UX Design -- Information related to UX design, design of the application
          Security Scanning -- Any requirements for Security Scanning
          Integrations -- List of all the third-party integrations required, list should be bulleted
          Support Details -- Post production activities, services, support required.
          Warranty Period or Defect Liability Period -- Support Period information, timeframe details for rectifying any defects post Production. 
          Forms -- Any forms to be developed
          Support For Existing System -- Existing application, system, support required
          Analytics - Analytics features and functionalities required
          Personalization -- Personalization Features and functionalities Required
          role: Requirements Analyser, Analyst, Information Retriever
          content: {content}
          """    
    prompt = PromptTemplate.from_template(template=prompt_template)
    prompt_formatted_str: str = prompt.format(content = docs)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt_formatted_str)  
    return response.text

# input = st.text_input("Ask Me Query")

if st.button("Get Info"):
         documents = load_documents()
         if documents :
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
                    file_name=f"response_presale_{uploaded_file.name}",
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
