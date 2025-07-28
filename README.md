# 🔍 Insight Retriever

Insight Retriever is a lightweight, open-source **Retrieval-Augmented Generation (RAG)** system built to ingest, semantically chunk, embed, and retrieve insights from unstructured documents like **PDFs, CSVs, and TXT files**. It enables users to ask natural language questions and receive intelligent, context-aware answers sourced directly from their own documents — without relying on paid APIs like OpenAI.

---

## 🎯 Use Cases

Insight Retriever is designed for real-world scenarios such as:

### 🏢 Business & Enterprise
- Internal document search (HR, Legal, SOPs)
- Auto-answering employee FAQs
- Extracting KPIs from reports and spreadsheets

### 📈 Data & Research Teams
- Automated Q&A from market research PDFs
- Summarizing survey results in CSVs
- Fast retrieval of findings from technical papers

### 🎓 Academic & Educational
- Literature review automation
- Contextual question answering from lecture notes
- Parsing and querying research papers

---

## 🧠 What It Does

Insight Retriever performs the following steps:

### 1. 📂 Ingest Documents
Supports:
- `PDF` – via PyMuPDF or PDFMiner
- `CSV` – via Pandas
- `TXT` – plain text files

### 2. ✂️ Semantic Chunking
Documents are split into **meaningful chunks** based on context, not arbitrary size. This improves retrieval accuracy and LLM understanding.

### 3. 📐 Embedding with MiniLM
Each chunk is embedded using **MiniLM**, a small yet powerful transformer model that generates dense vector representations.

### 4. ⚡ Fast Similarity Search with FAISS
Embeddings are stored in a **FAISS index** for efficient nearest-neighbor search at scale.

### 5. 🔁 RAG (Retrieval-Augmented Generation)
When a user asks a question:
- Related chunks are retrieved using vector similarity.
- These chunks are passed into **Flan-T5** (a lightweight open-source LLM from Google) via a **LangChain RAG pipeline**.
- The model generates a grounded, context-aware answer.

---

## 🛠️ Tech Stack

| Component        | Tool/Library            | Purpose                                      |
|------------------|--------------------------|----------------------------------------------|
| Language Model   | Flan-T5 (HuggingFace)    | Generates final answers                      |
| Embeddings       | MiniLM                   | Converts chunks into vectors                 |
| Vector Store     | FAISS                    | Fast similarity search                       |
| Orchestration    | LangChain                | RAG pipeline setup                           |
| Deployment       | AWS SageMaker (optional) | Cloud deployment                             |
| Data Parsers     | PyMuPDF, Pandas          | Parse PDF, CSV, TXT                          |

---

## ⚙️ How It Works

      ┌────────────┐
      │  Upload    │
      │ PDF/CSV/TXT│
      └────┬───────┘
           │
   ┌───────▼────────┐
   │ Semantic Chunk │
   └───────┬────────┘
           │
  ┌────────▼─────────┐
  │ Embed with MiniLM│
  └────────┬─────────┘
           │
     ┌─────▼─────┐
     │ FAISS     │◄──────────────┐
     │ Vector DB │               │
     └─────┬─────┘               │
           │                    │
      ┌────▼────┐         ┌─────▼────┐
      │ Retrieve │◄──────▶│  Query   │
      └────┬────┘         └──────────┘
           │
 ┌─────────▼─────────┐
 │ Generate with     │
 │ Flan-T5 (via RAG) │
 └─────────┬─────────┘
           │
     ┌─────▼─────┐
     │  Answer   │
     └───────────┘
