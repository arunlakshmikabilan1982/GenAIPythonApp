from pathlib import Path

from langchain.chains import ConversationalRetrievalChain

#used dependencies
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
import json
from flask import Flask , jsonify
from flask import json,request
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
    print(result)
    return result

class LLMResponseArticle:
      def __init__(self, ArticleTitle, ArticleBody,ArticleHeadline,ArticleLeadParagraph,ArticleExplanation):
       self.ArticleTitle = ArticleTitle
       self.ArticleBody = ArticleBody
       self.ArticleHeadline = ArticleHeadline
       self.ArticleLeadParagraph = ArticleLeadParagraph
       self.ArticleExplanation = ArticleExplanation

@app.route('/contentgeneratorbot', methods=['POST']) 
def contentgenerator_ai():

    #   return retriever_llm(queryfromfe)
    data = request.get_json()
    print(data)
    queryfromfe = data['queryfromfe']
    contenttype = data['contenttype']
    format_type = data['format_type']
    retriever = retriever_existingdb()
    response = contentgenerator_llm(retriever, queryfromfe, contenttype, format_type)
    #    print(result)
    #    return result
    #    articleTitle = "" ; articleBody = "" ; articleHeadline = "" ; articleLeadParagraph = "" ; articleExplanation = ""

    #    if contenttype == "article":
    #         if format == "template1":
    #           articleTitle = result.split("ArticleBody--")[0]
    #           articleBody = result.split("ArticleBody--")[1]
    #         if format == "template2":
    #           articleLeadParagraphSplit = result.split("ArticleLeadParagraph--")
    #           articleExplanationSplit = articleLeadParagraphSplit[1].split("ArticleExplanation--")
    #           articleHeadline = articleLeadParagraphSplit[0]
    #           articleLeadParagraph = articleExplanationSplit[0]
    #           articleExplanation = articleExplanationSplit[1]
            
    #         response = jsonify({"ArticleTitle":articleTitle,"ArticleBody":articleBody,"ArticleHeadline":articleHeadline,
    #                             "ArticleLeadParagraph":articleLeadParagraph,"ArticleExplanation":articleExplanation})
    #         return response
    #    if contenttype == "blog":
    #         response = jsonify({"ArticleTitle":articleTitle,"ArticleBody":articleBody,"ArticleHeadline":articleHeadline,
    #                             "ArticleLeadParagraph":articleLeadParagraph,"ArticleExplanation":articleExplanation})
    return response

# @app.route('/askaibot/<queryfromfe>') 
# def query_ai(queryfromfe):
#     #   return retriever_llm(queryfromfe)
#     #    retriever = retriever_existingdb()
    #    return query_llm(retriever, queryfromfe)

if __name__ == '__main__':
    #
    app.run(host="localhost", port=8000)
    