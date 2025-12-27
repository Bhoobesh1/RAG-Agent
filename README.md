# RAG(Retrieval-Augmented Generation)
# Web-Based PDF Question Answering System
<img width="1891" height="871" alt="image" src="https://github.com/user-attachments/assets/2ee9557e-c28b-40e7-908b-abb6918d4b18" />

# 📄 PDF Question Answering System

A web-based **PDF Question Answering System** that allows users to upload PDF documents and ask questions directly related to the uploaded content. The system uses **AI-powered semantic search and language models** to generate accurate answers based strictly on the document context.

---

## Features

- 📤 Upload PDF files (PDF format only)
- 🧠 AI-powered question answering from document content
- 🔍 Semantic search using vector embeddings (FAISS)
- 💬 Chat-style question and answer interface
- 🗣️ Handles basic small talk (greetings, thanks, etc.)
- ✅ Real-time PDF processing confirmation
- 🎨 Modern dark-themed user interface

---

## Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **PDF Processing:** PyPDF2  
- **Vector Database:** FAISS  
- **Embeddings & LLM:** OpenAI API  
- **AI Architecture:** Retrieval-Augmented Generation (RAG)

---

##  How It Works

1. User uploads a PDF document.
2. Text is extracted from the PDF.
3. The text is split into smaller chunks.
4. Each chunk is converted into vector embeddings using OpenAI.
5. Embeddings are stored in a FAISS vector index.
6. When a question is asked:
   - Relevant chunks are retrieved using semantic similarity.
   - The AI model generates an answer using only the retrieved content.
7. General greetings or casual messages are handled separately using small-talk logic.

---

##  User Interface Overview

- PDF upload section with file size validation
- Status message after successful PDF processing
- Chat window displaying:
  - User questions
  - AI-generated answers
- Input field to ask questions related to the uploaded PDF

---

## Use Cases

- 📘 Academic and study material Q&A
- 📄 Company policy and documentation analysis
- 📚 Research paper understanding
- 🤖 AI-based document assistant systems

---

##  Limitations

- Answers are limited to the uploaded PDF content
- Requires a valid OpenAI API key
- Large PDF files may increase processing time

---

##  Environment Setup

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key"

