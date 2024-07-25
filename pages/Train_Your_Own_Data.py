import os
from pathlib import Path
from datetime import datetime
import streamlit as st
from bs4 import BeautifulSoup

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders.sitemap import SitemapLoader
from Navigation import sidebar

sidebar()

# Initialize Streamlit page
# st.set_page_config(page_title="Infant Food Recipes")

# Load environment variables
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_INDEX = st.secrets["PINECONE_INDEX"]
DOC_DIR_PATH = st.secrets["DOC_DIR_PATH"]

current_time = datetime.now()
formatted_time = current_time.strftime("%y%m%H%M")
# Define paths
TMP_DIR = Path(__file__).resolve().parent.parent.joinpath('documents',formatted_time)
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Function to load uploaded documents
def load_documents():
    loader = DirectoryLoader(TMP_DIR.as_posix(), glob='**/*.pdf')
    documents = loader.load()
    return documents

# Function to split documents into texts
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=50, separators=[" ", ",", "\n"])
    texts = text_splitter.split_documents(documents)
    return texts

# Function to remove navigation and header elements from HTML content
def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    nav_elements = content.find_all("nav")
    header_elements = content.find_all("header")

    for element in nav_elements + header_elements:
        element.decompose()

    return str(content.get_text())

# Function to upload embeddings to Pinecone
def embeddings_on_pinecone(texts):
    embeddings = HuggingFaceEmbeddings()
    PineconeVectorStore.from_documents(texts, embeddings, index_name=PINECONE_INDEX)

# Function to process uploaded documents
def process_documents():
   try:
        for source_doc in st.session_state.source_docs:
            #
            save_path = Path(TMP_DIR, source_doc.name)
            with open(save_path, mode='wb') as w:
             w.write(source_doc.getvalue())
            #
            documents = load_documents()
            #
            texts = split_documents(documents)
            #
            st.session_state.retriever = embeddings_on_pinecone(texts)
   except Exception as e:
            st.error(f"An error occurred: {e}")   

# Function to process documents from a sitemap URL
def process_sitemapdocs():
    try:
        sitemap_loader = SitemapLoader(
            st.session_state.sitemapurl,
            parsing_function=remove_nav_and_header_elements,
            filter_urls=["https://www.concentrix.com/solutions", "https://www.concentrix.com/partners"]
        )
        documents = sitemap_loader.load()
        texts = split_documents(documents)
        embeddings_on_pinecone(texts)
        st.success("The sitemap documents have been processed successfully, and vector stores have been created")
        st.session_state.retriever = True  # Indicate successful processing
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.retriever = False  # Indicate failure

# Function to initialize the application
def boot():
    st.title("Train your own Data")

    # File upload section
    st.session_state.source_docs = st.file_uploader(label="Please select the file you would like to upload.", type="pdf")

    if st.button("Submit Documents") :
     with st.spinner("Uploading the Data..."):
        if st.session_state.source_docs is not None and st.session_state.source_docs != "":
            process_documents()

        else:
            st.warning("Please upload the file")

    # Sitemap URL input section
    st.session_state.sitemapurl = st.text_area("Please enter the Sitemap Url", key="query_input")
    # st.session_state.sitemapurl = st.text_input("Provide Sitemap Url")

    if st.button("Submit Sitemap URL"):
       with st.spinner("Uploading the Data..."): 
        if st.session_state.sitemapurl is not None and st.session_state.sitemapurl != "":
            process_sitemapdocs()
    
        else:
            st.warning("Please upload the url")

if __name__ == '__main__':
    boot()
