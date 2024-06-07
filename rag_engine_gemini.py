import os
import pinecone
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import  Pinecone
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import Pinecone
from langchain.prompts import ChatPromptTemplate
# from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai


from environment import GEMINI_API_KEY, PINECONE_INDEX

TMP_DIR = Path(__file__).resolve().parent.joinpath('data', 'tmp')

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="RAG")
st.title("CNX Malls Info AI ChatBot")

# def find_indexs():
#     pinecone_client = pin(api_key='6a2024cb-08ce-4933-8e2b-9c410713fe59')
#     for index in pinecone_client.list_indexes():
#         st.write(index['index'])

def retrive_data():
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001',google_api_key=GEMINI_API_KEY)
    # embeddings = HuggingFaceEmbeddings()
    vectordb = Pinecone.from_existing_index(index_name=PINECONE_INDEX, embedding=embeddings)
    retriever = vectordb.as_retriever() 
    return retriever

def query_llm(retriever, query):
    general_system_template = r""" 
    Given a specific context, Provide 10 seperate paragraphed Answers except for Events.
    Do not provide paragraphed answers for Events related queries.
    Generate content as specified for Article, Blog queries and use Article and Blog generic templates, generate Article and Blog content based on requested timeframe. do not use numbering.
    Do not generate content for multiple events. 
    For Events use below Template to answer, Generate More Content for one asked event and fetch event based on requested timeframe.
    Event Title:
    Description:
    Date and Time:
    Location:
    ----
    {context}
    ----
    """

    general_ai_template = "role:content creator"
    general_user_template = "Question:```{query}```"
    messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template),
            AIMessagePromptTemplate.from_template(general_ai_template)
               ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)
    model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest",
                            google_api_key=GEMINI_API_KEY,
                            temperature=0.2,
                            convert_system_message_to_human=True)
    qa = ConversationalRetrievalChain.from_llm(
                    llm=model,
                    retriever=retriever,
                    chain_type="stuff",
                    verbose=True,
                    combine_docs_chain_kwargs={'prompt': qa_prompt}
                )
    result = qa({"question": query, "query": query, "chat_history": st.session_state.messages})
    result = result["answer"]
    return result

def process_documents():
        try:
            st.session_state.retriever = retrive_data()
        except Exception as e:
            st.error(f"An error occurred: {e}")

if query := st.chat_input("User Input", key="user_input"):
    if "retriever" not in st.session_state:
        process_documents()

    if "messages" not in st.session_state:
        st.session_state.messages = []    
    for message in st.session_state.messages:
        st.chat_message('human').write(message[0])
        st.chat_message('ai').write(message[1])

    if query :
        st.chat_message("human").write(query)
        response = query_llm(st.session_state.retriever, query)
        st.chat_message("ai").write(response)
    