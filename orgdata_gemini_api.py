#used dependencies
from pathlib import Path
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from flask import Flask, json, request
app = Flask(__name__)

from environment import PINECONE_INDEX, GEMINI_API_KEY

TMP_DIR = Path(__file__).resolve().parent.joinpath('data', 'tmp')

with open('./data/prompttemplates.json') as json_data:
      prompts = json.load(json_data)

model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest",
                            google_api_key=GEMINI_API_KEY,
                            temperature=0.2,
                            convert_system_message_to_human=True)

def retriever_existingdb():
    embeddings = HuggingFaceEmbeddings()
    vectorstore = PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX, embedding=embeddings)
    retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
    )
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

def contentgenerator_llm(retriever, query, contenttype, format):

    general_system_template =  prompts[contenttype][format] + r"""
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

@app.route('/contentgeneratorbot', methods=['POST']) 
def contentgenerator_ai():
    data = request.get_json()
    print(data)
    queryfromfe = data['Query']
    contenttype = data['ContentType']
    format_type = data['FormatType']
    retriever = retriever_existingdb()
    response = contentgenerator_llm(retriever, queryfromfe, contenttype.lower(), format_type.lower())
    return response

@app.route('/askaibot', methods=['POST'])
def query_ai():
       data = request.get_json()
       queryfromfe = data['query']
       retriever = retriever_existingdb()
       return query_llm(retriever, queryfromfe)

if __name__ == '__main__':
    #
    app.run(host="localhost", port=8000)
    