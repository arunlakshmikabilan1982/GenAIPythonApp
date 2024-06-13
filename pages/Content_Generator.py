import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
import json

GEMINI_API_KEY="AIzaSyDcF1LrSLzb9l3B7NfS_5LFNyoGnMv6K_g"
PINECONE_INDEX="geminiindex"


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
contenttype = st.selectbox("Content Type", ["article", "blog"])  # Assuming you have these options
format_type = st.selectbox("Format Type", ["template1", "template2"])  # Assuming you have these options

if st.button("Generate Content"):
    retriever = retriever_existingdb()
    response = contentgenerator_llm(retriever, queryfromfe, contenttype, format_type)
    st.write("Response:", response)