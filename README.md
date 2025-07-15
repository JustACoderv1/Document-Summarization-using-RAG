# PDF Summary using RAG

This project provides an end-to-end pipeline to **extract**, **embed**, **retrieve**, and **summarize** content from PDF and Word documents using:

- 📄 `PyPDF2` and `python-docx` for document parsing  
- 🧠 `SentenceTransformer` (SBERT) for semantic embeddings  
- ⚡ `FAISS` for fast similarity search  
- 🤖 Google Gemini (`google.generativeai`) for LLM-based summarization

---

## 🔍 Key Features

- ✅ Supports both **PDF** and **DOCX** documents
- 🧠 Sentence-BERT-based embedding generation
- 🔎 Vector search with **FAISS**
- 📡 Summarization via **Google Gemini API**
- 🧰 Modular code structure for reuse

---

## 🚀 Workflow

1. **Extract** text from a PDF or DOCX file  
2. **Split** text into semantic chunks or sentences  
3. **Generate** embeddings using Sentence-BERT  
4. **Index** and search using FAISS (optional)  
5. **Summarize** using Google Gemini API

---

## 📦 Requirements

```bash
pip install -r requirements.txt
