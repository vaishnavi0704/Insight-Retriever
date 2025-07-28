import streamlit as st
from rag_pipeline import load_faiss_index, get_answer

# Load FAISS and Retriever
faiss_index = load_faiss_index()
retriever = faiss_index.as_retriever()

st.title(" Multi-Modal Corporate RAG System (Free LLM)")

query = st.text_input("Enter your query:")

if query:
    answer = get_answer(query, retriever)  # Now this returns a string, not 'docs'
    st.subheader("Answer:")
    st.write(answer)

st.sidebar.info("Place your documents in the /data folder.")
