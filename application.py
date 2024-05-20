from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.schema import Document
import os
# from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
import db_connection as dbc
import sqlite3

def setup_environment():
    load_dotenv()

def setup_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    return GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.5, verbose=True)

def load_qadb():
    cursor, conn = dbc.create_connection()
    dbc.load_tables(cursor, conn)
    li_qadb = dbc.show_qadb(cursor, conn)
    dbc.close_connection(cursor, conn)
    return li_qadb

def load_txt(li):
    # print(li)
    documents = [Document(page_content=str(row)) for row in li]
    print(documents)
    return documents


def create_embeddings_and_retriever(data):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
    return vectordb.as_retriever(score_threshold=0.7)

def create_prompt_and_chain(llm, retriever):
    prompt_template = """
INSTRUCTIONS:
You are a helpful human-like assistant. Your task is to generate an answer based on the given context and question. Follow these guidelines:

1. Use only the provided context to answer the question. Do not make up or fabricate information.
2. If the answer is not found in the context, respond with "I don't know."
3. In your answer, try to provide as much relevant text as possible from the "response" section of the source document context, without making significant changes.
4. Structure your answer in a clear and easy-to-understand manner for the user.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}

    return RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=retriever,
                                    input_key="query",
                                    return_source_documents=True,
                                    chain_type_kwargs=chain_type_kwargs)

def chat(chain):
    while True:
        que = input('Ask a question : ')
        if que.lower() == "x":
            break
        else:
            k = chain.invoke(que.strip())
            print(k.get('result'))


setup_environment()
llm = setup_llm()

li_qadb = load_qadb()
data = load_txt(li_qadb)

# print(data)
retriever = create_embeddings_and_retriever(data)
chain = create_prompt_and_chain(llm, retriever)
# chat(chain)

def generate_response(question="hi"):
    k = chain.invoke(question.strip())
    response= k.get('result')
    return response

# generate_response()