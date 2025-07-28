from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
import pandas as pd
import os

# Embedding Model
model_name = "all-MiniLM-L6-v2"
embedder = HuggingFaceEmbeddings(model_name=model_name)

# ------------ Data Loaders ------------
def load_text_docs():
    docs = []
    for file in os.listdir("data/docs"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join("data/docs", file))
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(os.path.join("data/docs", file))
            docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

def load_table_docs():
    docs = []
    for file in os.listdir("data/tables"):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join("data/tables", file))
            docs.append(Document(page_content=df.to_string(), metadata={"source": file}))
    return docs

def build_faiss_index():
    text_docs = load_text_docs()
    table_docs = load_table_docs()
    all_docs = text_docs + table_docs
    db = FAISS.from_documents(all_docs, embedder)
    db.save_local("faiss_index")
    return db

def load_faiss_index():
    if not os.path.exists("faiss_index"):
        return build_faiss_index()
    return FAISS.load_local("faiss_index", embedder ,allow_dangerous_deserialization=True)

# ------------ LLM Integration ------------
def get_llm():
    flan_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", max_new_tokens=500)
    return HuggingFacePipeline(pipeline=flan_pipeline)

# ------------ Query Processor ------------
def get_answer(query, retriever):
    llm = get_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )
    result = qa_chain.run(query)
    return result
