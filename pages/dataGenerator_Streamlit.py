from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import PromptTemplate
# from environment import PINECONE_SEO_INDEX, GEMINI_API_KEY, PINECONE_API_KEY
import base64
from PIL import Image
import io
import numpy as np
import streamlit as st
import openpyxl
import tempfile
import requests
from io import StringIO
import urllib
from langchain.chains import RetrievalQA

PINECONE_API_KEY = "610b639f-dad6-48f9-a78a-7a55ca351a4c"
PINECONE_SEO_INDEX = "seometadata"
GEMINI_API_KEY="AIzaSyDcF1LrSLzb9l3B7NfS_5LFNyoGnMv6K_g"


pc = Pinecone(api_key=PINECONE_API_KEY)
# pineconeindex = pc.Index(PINECONE_SEO_INDEX)
genai.configure(api_key=GEMINI_API_KEY)
 
def imagetotext(imageurl):
      response = requests.get(imageurl)
    #   converted_string = base64.b64encode(imageurl.read()) 
    #   print(converted_string)
      image = Image.open(requests.get(imageurl, stream=True).raw)
      prompt_template: str = r"""
          Given a specific context, Generate SEO Metadata details, Strictly Use below Template:
          Title: eyecatching title for the image, should be atleast 5 words
          Description: All the important details like configuration,features about the image, Not to exceed 50 words, should be in paragraph
          Keywords: keywords for the image provided
          role: Metadata Content Creator
          question: {question}
          """    
      prompt = PromptTemplate.from_template(template=prompt_template)
      input = "follow template and role provided"
      prompt_formatted_str: str = prompt.format(question=input)
      model = genai.GenerativeModel('gemini-pro-vision')
      response = model.generate_content([prompt_formatted_str,image])  
      return response.text

def load_pdf_documents(uploaded_file):
    uploaded_file = "https://iris.who.int/bitstream/handle/10665/310944/9789241515085-eng.pdf"
    loader = PyPDFLoader(uploaded_file, extract_images=True)
    documents = loader.load()
    return documents

model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest",
                            google_api_key=GEMINI_API_KEY,
                            temperature=0.2,
                            convert_system_message_to_human=True)

# model = genai.GenerativeModel('gemini-pro-vision')

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=50,separators=[" ", ",", "\n"])
    texts = text_splitter.split_documents(documents)
    return texts

def embeddings_on_pinecone(texts):
    embeddings = HuggingFaceEmbeddings()
    if(PINECONE_SEO_INDEX in pc.list_indexes().names()):
        print(pc.describe_index(PINECONE_SEO_INDEX))
        pc.delete_index(PINECONE_SEO_INDEX)
    pc.create_index(
    name=PINECONE_SEO_INDEX,
    dimension=768,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    )
    PineconeVectorStore.from_documents(texts, embeddings, index_name=PINECONE_SEO_INDEX)

def retriever_existingdb():
    embeddings = HuggingFaceEmbeddings()
    vectorstore = PineconeVectorStore.from_existing_index(index_name=PINECONE_SEO_INDEX, embedding=embeddings)
    retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
    )
    return retriever

def query_llm(retriever, query):
    general_system_template = r""" 
    Given a specific context, Generate SEO Metadata details, Strictly Use below Template:
    Title-- eyecatching title for the image, should be atleast 5 words
    Description-- All the important details like configuration,features about the image, Not to exceed 50 words, should be in paragraph
    Keywords-- keywords for the image provided
    ----
    {context}
    ----
    """

    general_ai_template = "role:SEO metadata content creator"
    general_user_template = "Question:```{query}```"
    messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template),
            AIMessagePromptTemplate.from_template(general_ai_template)
               ]
    qa_prompt = ChatPromptTemplate.from_messages( messages )
 
    qa = ConversationalRetrievalChain.from_llm(
            model,
            retriever=retriever,
            chain_type="stuff",
            verbose=True,
            combine_docs_chain_kwargs={'prompt': qa_prompt}
        )
    
    result = qa({"question": query, "query": query, "chat_history": ""})
    result = result["answer"]
    return result

def process_pdf_documents(uploaded_file):
    documents = load_pdf_documents(uploaded_file)
    texts = split_documents(documents)
    embeddings_on_pinecone(texts)
    retriever  =  retriever_existingdb()
    query = "generate SEO Metadata details as per requested template"
    results = query_llm(retriever, query)
    return results

# File uploader
# uploaded_file = st.file_uploader("Choose the file to upload")

# if uploaded_file is not None:
#   print(uploaded_file)
#   results = process_pdf_documents(uploaded_file)
#   print(results)

def main():
    st.title("Choose the file to upload")
    st.subheader("File Data")
    uploaded_file = st.file_uploader("Choose the file to upload")
    if uploaded_file is not None:
        st.write(uploaded_file)
        results = process_pdf_documents(uploaded_file)
        st.write(results)
        
if __name__ == "__main__":
    main()
    