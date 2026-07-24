# AI Document Intelligence Assistant

A Streamlit web app that lets you upload PDF documents and ask questions about them using Retrieval-Augmented Generation (RAG).

Upload a PDF → extract & chunk text → create embeddings → store in FAISS → retrieve relevant context → answer with Google Gemini.

---

## Features

- User authentication (signup / login / logout) with bcrypt password hashing
- PDF upload with validation (type + size)
- Document processing pipeline (extract → clean → chunk → embed → FAISS)
- Per-document chat grounded in uploaded content
- Document list with chat and delete
- Analytics dashboard (documents, chats, messages, storage)
- SQLite persistence for users, documents, conversations, and messages

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| UI | Streamlit |
| Auth | bcrypt + Streamlit session state |
| Database | SQLite + SQLAlchemy |
| PDF extraction | PyMuPDF (`fitz`) |
| Chunking | LangChain Text Splitters |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector store | FAISS |
| LLM | Google Gemini |

---

## Project Structure

```text
├── app.py                          # Landing page
├── pages/
│   ├── login.py
│   ├── signup.py
│   ├── dashboard.py
│   ├── upload.py
│   ├── my_document.py
│   ├── chat.py
│   └── analytics.py
├── authentication/                 # Password hashing + session helpers
├── config/                         # Environment settings
├── database/                       # SQLAlchemy engine + DB init
├── models/                         # User, Document, Conversation, Message
├── repositories/                   # Database access layer
├── services/
│   ├── ai/                         # RAG, retrieval, Gemini
│   └── processing/                 # PDF → clean → chunk → embed → FAISS
├── storage/                        # File storage helpers + uploads/vector data
├── utils/                          # Auth guard
├── .env.example
├── requirements.txt
└── .streamlit/config.toml
```

---

## Prerequisites

- Python 3.10+ (tested with 3.13)
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/AdityaGadbail/AI-Document-Intelligence-Assistant.git
cd "AI Document Intelligence Assistant"
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> First run may download the Sentence Transformers embedding model automatically.

### 4. Configure environment variables

Copy the example file and add your API key:

```bash
copy .env.example .env
```

Edit `.env`:

```env
MAX_UPLOAD_SIZE=20971520
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

GEMINI_API_KEY=AIzaSy...your_key_here...
GEMINI_MODEL=gemini-2.5-flash

EMBEDDING_MODEL=all-MiniLM-L6-v2
ALLOWED_EXTENSIONS=.pdf

UPLOAD_DIRECTORY=storage/uploads
VECTOR_STORE_DIRECTORY=storage/vector_store
```

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google AI Studio API key (required) | — |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.5-flash` |
| `MAX_UPLOAD_SIZE` | Max PDF size in bytes | `20971520` (20 MB) |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `EMBEDDING_MODEL` | Sentence Transformers model | `all-MiniLM-L6-v2` |
| `ALLOWED_EXTENSIONS` | Allowed file extensions | `.pdf` |
| `UPLOAD_DIRECTORY` | Where PDFs are stored | `storage/uploads` |
| `VECTOR_STORE_DIRECTORY` | Where FAISS indexes are stored | `storage/vector_store` |

> Gemini keys from AI Studio usually start with `AIza`. Keep `.env` private and never commit it.

### 5. Initialize the database

```bash
python -m database.init_db
```

This creates `storage/app.db` and all tables.

### 6. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## How to Use

1. Create an account or log in
2. Open **Upload Documents** and upload a PDF
3. Wait until processing finishes (`READY` status)
4. Go to **My Documents** → click **Chat**
5. Ask questions about the document
6. Optionally check **Analytics** for usage stats

Answers are generated only from retrieved document context. If the answer is not in the PDF, the assistant says it could not find the information.

---

## Architecture Overview

```text
User (Streamlit UI)
        │
        ▼
   Services layer
        │
        ├── AuthService
        ├── DocumentService ──► DocumentProcessor
        │                         ├── PDFExtractor
        │                         ├── TextCleaner
        │                         ├── TextChunker
        │                         ├── EmbeddingService
        │                         └── VectoreStore (FAISS)
        ├── ConversationService / MessageService
        ├── RagService
        │     ├── RetrievalService
        │     └── GeminiService
        └── AnalyticsService
        │
        ▼
 Repositories → SQLAlchemy models → SQLite
```

---

## Document Processing Flow

1. Validate PDF and save file to disk
2. Create document record (`UPLOADED` → `PROCESSING`)
3. Extract text with PyMuPDF
4. Clean and split into overlapping chunks
5. Generate embeddings with Sentence Transformers
6. Save FAISS index + chunk metadata per document
7. Mark document as `READY`

---

## Chat / RAG Flow

1. Create or reuse a conversation for the selected document
2. Save the user question
3. Embed the question and search FAISS for top matching chunks
4. Build a grounded prompt with retrieved context
5. Generate an answer with Gemini
6. Save the assistant reply and show sources

---

## Notes

- Database path is `sqlite:///storage/app.db`
- Uploaded files live under `storage/uploads/`
- Vector indexes live under `storage/vector_store/doc_<id>/`
- Deleting a document removes its DB row, file, and vector store data
- Large PDFs process synchronously during upload, so the UI may wait while embedding runs

---

## Troubleshooting

**`API_KEY_INVALID`**
- Confirm `GEMINI_API_KEY` in `.env` is a valid AI Studio key (`AIza...`)
- Restart Streamlit after changing `.env`

**`Gemini API key missing`**
- Ensure `.env` is in the project root and contains `GEMINI_API_KEY=...`

**Upload / import errors related to storage**
- Make sure `storage/storage_service.py` exists
- Ensure `storage/uploads` and `storage/vector_store` can be created

**Embedding model download is slow**
- First run downloads `all-MiniLM-L6-v2` from Hugging Face; later runs use the cache

**Database tables missing**
- Run: `python -m database.init_db`

---


Made by Aditya Gadbail
