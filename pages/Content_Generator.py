import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
import json
import asyncio
# Create a new event loop
loop = asyncio.new_event_loop()
# Set the event loop as the current event loop
asyncio.set_event_loop(loop)

# from environment import PINECONE_INDEX, GEMINI_API_KEY

from dotenv import load_dotenv
import os


load_dotenv()  


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_SEO_INDEX = os.getenv("PINECONE_SEO_INDEX")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_SEO_INDEX = st.secrets["PINECONE_SEO_INDEX"]
PINECONE_INDEX = st.secrets["PINECONE_INDEX"]


# Load prompts from JSON file
with open('./data/prompttemplates.json') as json_data:
    prompts = json.load(json_data)

# Initialize Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest",
                               google_api_key=GEMINI_API_KEY,
                               temperature=0.2,
                               convert_system_message_to_human=True)

# Initialize retriever
def retriever_existingdb():
    embeddings = HuggingFaceEmbeddings()
    vectorstore = PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})
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
    qa_prompt = ChatPromptTemplate.from_messages( messages )
 
    qa = ConversationalRetrievalChain.from_llm(
            llm=model,
            retriever=retriever,
            chain_type="stuff",
            verbose=True,
            combine_docs_chain_kwargs={'prompt': qa_prompt}
        )
    result = qa({"question": query, "query": query, "chat_history": ""})
    result = result["answer"]
    return result

# Define content generator function
def contentgenerator_llm(retriever, query, contenttype, format):
    general_system_template = prompts[contenttype][format] + r"""
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

    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        combine_docs_chain_kwargs={'prompt': qa_prompt}
    )
    result = qa({"question": query, "query": query, "chat_history": ""})
    result = result["answer"]
    return result

# Streamlit UI
st.title("Chat with Organizational Data")

# Content Generator Functionality
queryfromfe = st.text_input("Enter your query:")
querybytype = st.checkbox("QueryByType: Article or Blog")


if querybytype:
    contenttype = st.selectbox("Content Type", ["Article", "Blog"])  # Assuming you have these options
    format_type = st.selectbox("Format Type", ["Template1", "Template2"])  # Assuming you have these options

    if(contenttype == "Article" and format_type == "Template1"):
        st.text("Article Template 1:\nArticle Title \n" +
                                "Article Body \n")
    
    if(contenttype == "Article" and format_type == "Template2"):
        st.text("Article Template 2:\nArticle Headline \n" +
                                "Article LeadParagraph \n" +
                                "Article Explanation \n")   
    
    if(contenttype == "Blog" and format_type == "Template1"):
        st.text("Blog Template 1:\nBlog Title \n" +
                                "Blog Body \n")
    
    if(contenttype == "Blog" and format_type == "Template2"):
        st.text("Blog Template 2:\nBlog Title \n" +
                                "Blog High-lights \n" +
                                "Blog Body \n") 


if st.button("Generate Content"):
    retriever = retriever_existingdb()
    if(querybytype == True):
       response = contentgenerator_llm(retriever, queryfromfe, contenttype.lower(), format_type.lower())
    else:
       response = query_llm(retriever, queryfromfe)
    st.write("Response:", response)