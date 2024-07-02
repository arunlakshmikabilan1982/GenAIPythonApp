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

# Define paths
TMP_DIR = Path(__file__).resolve().parent / 'documents' / datetime.now().strftime("%y%m%H%M")
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Function to load uploaded documents
def load_documents():
    loader = DirectoryLoader(TMP_DIR, glob='**/*.pdf')
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
        documents = load_documents()
        texts = split_documents(documents)
        embeddings_on_pinecone(texts)
        st.success("Documents processed successfully and vector stores created.")
        st.session_state.retriever = True  # Indicate successful processing
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.retriever = False  # Indicate failure

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
        st.success("Sitemap documents processed successfully and vector stores created.")
        st.session_state.retriever = True  # Indicate successful processing
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.retriever = False  # Indicate failure

# Function to initialize the application
def boot():
    st.title("Upload Documents and Provide Sitemap URL")

    # File upload section
    st.session_state.source_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True)

    if st.button("Submit Documents"):
        process_documents()

    # Sitemap URL input section
    st.session_state.sitemapurl = st.text_input("Provide Sitemap Url")

    if st.button("Submit Sitemap URL"):
        process_sitemapdocs()

    # if st.session_state.get("retriever") is True:
    #     st.success("Files and Sitemap data processed successfully.")
    # elif st.session_state.get("retriever") is False:
    #     st.error("Processing failed. Please check your input and try again.")

if __name__ == '__main__':
    boot()
