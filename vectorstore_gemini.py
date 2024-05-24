import os, tempfile
import pinecone
from pathlib import Path

from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.llms.openai import OpenAIChat
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


#used dependencies
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings


from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders.sitemap import SitemapLoader
from datetime import datetime
import nest_asyncio
from bs4 import BeautifulSoup

nest_asyncio.apply()
import streamlit as st

from environment import OPENAI_API_KEY, \
    PINECONE_API_KEY, PINECONE_ENVIRONMENT, \
    PINECONE_INDEX, DOC_DIR_PATH, OPENAI_EMBEDDING_MODEL, GEMINI_API_KEY

LOCAL_VECTOR_STORE_DIR = Path(__file__).resolve().parent.joinpath('data', 'vector_store')
genai.configure(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
pineconeindex = pc.Index(PINECONE_INDEX)

current_time = datetime.now()
formatted_time = current_time.strftime("%y%m%H%M")
# if today.hour < 12:
#     h = "00"
# else:
#     h = "12"
uploadpath = DOC_DIR_PATH + formatted_time
if not os.path.exists(uploadpath):
    os.mkdir(uploadpath)
# st.write(uploadpath)
# parent_path = Path(__file__).parent.resolve()
TMP_DIR = Path(__file__).resolve().parent.joinpath('documents',formatted_time)
st.set_page_config(page_title="Infant Food Recipes")
TMP_DIR1 = Path(__file__).resolve().parent.joinpath('data', 'tmp')
# TMP_DIR = Path(DOC_DIR_PATH)


st.title("Upload CNX Malls Related Documents and Provide Sitemap URL")

def load_documents():
    loader = DirectoryLoader(TMP_DIR.as_posix(), glob='**/*.pdf')
    documents = loader.load()
    return documents

def load_sitemap_documents():
    sitemap_loader = SitemapLoader(st.session_state.sitemapurl,
        parsing_function=remove_nav_and_header_elements,
        filter_urls=["https://www.concentrix.com/solutions","https://www.concentrix.com/partners"]
        )
    documents = sitemap_loader.load()
    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=50,separators=[" ", ",", "\n"])
    texts = text_splitter.split_documents(documents)
    return texts

def split_sitemap_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=50,separators=[" ", ",", "\n"])
    texts = text_splitter.split_documents(documents)
    return texts

def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Find all 'nav' and 'header' elements in the BeautifulSoup object
    nav_elements = content.find_all("nav")
    header_elements = content.find_all("header")

    # Remove each 'nav' and 'header' element from the BeautifulSoup object
    for element in nav_elements + header_elements:
        element.decompose()

    return str(content.get_text())

def embeddings_on_pinecone(texts):
    # pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    embeddings = HuggingFaceEmbeddings()
    #embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GEMINI_API_KEY)
    PineconeVectorStore.from_documents(texts, embeddings, index_name=PINECONE_INDEX)

def input_fields():
    #
    st.session_state.source_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True)
    #
    st.session_state.sitemapurl = st.text_input("Provide Sitemap Url")
    #

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
                # for _file in TMP_DIR.iterdir():
                #     temp_file = TMP_DIR.joinpath(_file)
                #     temp_file.unlink()
                #
                texts = split_documents(documents)
                #
                st.session_state.retriever = embeddings_on_pinecone(texts)
        except Exception as e:
            st.error(f"An error occurred: {e}")    

def process_sitemapdocs():
        try:    
               #
               documents = load_sitemap_documents()
               #
               texts = split_sitemap_documents(documents)
               #
               st.session_state.retriever = embeddings_on_pinecone(texts)
        except Exception as e:
            st.error(f"An error occurred: {e}")                

def boot():
    #
    input_fields()
    #
    st.button("Submit Documents", on_click=process_documents)
    #
    st.button("Submit Sitemap URL", on_click=process_sitemapdocs)
    #
    if "retriever" in st.session_state:
        st.write("Files Uploded Sucessfully and vector stores created")  
    #

if __name__ == '__main__':
    #
    boot()