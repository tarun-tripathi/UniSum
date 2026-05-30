# 🧠 UniSum — Multi-Source RAG Application

> An intelligent AI-powered backend that lets you **ask questions** from PDFs, Websites, and YouTube videos using Retrieval-Augmented Generation (RAG).

---

## 📌 What is UniSum?

UniSum is a **FastAPI-based RAG (Retrieval-Augmented Generation) system** that:
- 📄 Ingests **PDF documents**
- 🌐 Scrapes and understands **websites**
- 🎥 Extracts transcripts from **YouTube videos**
- 🤖 Uses **DeepSeek LLM** (via HuggingFace) to answer your questions based on the content

No hallucinations — the AI only answers from the content **you provide**.

---

## 🗂️ Project Structure

```
MultiSourceRAG/
├── main.py               # FastAPI app — all API endpoints
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not pushed to GitHub)
├── .env_example          # Template for environment variables
├── MANUAL_TESTING.md     # How to test the API manually
├── demo.txt              # Demo/test notes
├── test_api.sh           # Shell script for API testing
├── test_pdf.sh           # Shell script for PDF testing
├── uploads/              # Uploaded PDFs stored here
└── chroma_db/            # ChromaDB vector store (auto-generated)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI |
| **LLM** | DeepSeek-R1 (via HuggingFace Endpoint) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector Database** | ChromaDB |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Web Scraping** | LangChain WebBaseLoader |
| **YouTube** | youtube-transcript-api |
| **Orchestration** | LangChain |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/tarun-tripathi/UniSum.git
cd UniSum/MultiSourceRAG
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env_example .env
```

Open `.env` and add your HuggingFace API token:

```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

> Get your free token at: https://huggingface.co/settings/tokens

### 5. Run the Server

```bash
python main.py
```

Server will start at: **http://localhost:8000**

---

## 🔌 API Endpoints

### `GET /`
Health check — confirms server is running.

**Response:**
```json
{"message": "WELCOME TO MULTI-SOURCE RAG APPLICATION"}
```

---

### `POST /upload-pdf`
Upload a PDF file. Returns a `collection_name` to use for querying.

**Request:** `multipart/form-data`
```bash
curl -X POST -F "file=@your_file.pdf" http://localhost:8000/upload-pdf
```

**Response:**
```json
{"message": "abc123-uuid-collection"}
```

---

### `POST /pdf-rag`
Ask a question about an uploaded PDF.

**Request Body:**
```json
{
  "collection_name": "abc123-uuid-collection",
  "question": "What is the main topic of this document?"
}
```

**Response:**
```json
{"message": "The document is about..."}
```

---

### `POST /web-rag`
Load a website into the vector store.

**Request Body:**
```json
{
  "web_url": "https://example.com"
}
```

**Response:**
```json
{"message": "abc123-uuid-collection"}
```

---

### `POST /web-query`
Ask a question about a loaded website.

**Request Body:**
```json
{
  "collection_name": "abc123-uuid-collection",
  "question": "What is this website about?"
}
```

**Response:**
```json
{"message": "This website is about..."}
```

---

## 🧪 How to Test

### Option 1: Swagger UI (Easiest)
Open in browser: **http://localhost:8000/docs**

### Option 2: curl Commands
```bash
# Test welcome
curl http://localhost:8000/

# Load a website
curl -X POST http://localhost:8000/web-rag \
  -H "Content-Type: application/json" \
  -d '{"web_url": "https://python.org"}'

# Ask a question (use collection_name from above response)
curl -X POST http://localhost:8000/web-query \
  -H "Content-Type: application/json" \
  -d '{"collection_name": "your-id-here", "question": "What is Python?"}'
```

### Option 3: Postman / Insomnia
See `MANUAL_TESTING.md` for detailed Postman steps.

---

## 🔄 How It Works

```
User Input (PDF / URL / YouTube)
        ↓
  Content Extraction
  (PyMuPDF / WebBaseLoader / YouTubeTranscriptAPI)
        ↓
  Text Chunking
  (RecursiveCharacterTextSplitter — 450 tokens, 50 overlap)
        ↓
  Embedding Generation
  (sentence-transformers/all-MiniLM-L6-v2)
        ↓
  Stored in ChromaDB Vector Store
        ↓
  User asks a Question
        ↓
  Top-K Relevant Chunks Retrieved (k=5 for PDF, k=10 for web)
        ↓
  Passed to DeepSeek-R1 LLM with Prompt
        ↓
  Accurate, Grounded Answer Returned
```

---

## 🛡️ Notes

- The AI **only answers from provided content** — it will return `"no"` if the answer isn't found
- `chroma_db/` is auto-generated locally — don't delete it while server is running
- Keep your `.env` file **private** — never push it to GitHub
- The `uploads/` folder stores your PDFs temporarily

---

## 👥 Team

| Name | Enrollment No. |
|---|---|
| Tarun Tripathi | 0103AL221215 |
| Vishnu Kumar | 0103AL221229 |
| Vatsalya Shukla | 0103AL221224 |

**Guide:** Prof. HARSH NIGAM
**Institution:** Lakshmi Narain College of Technology, Bhopal
**Department:** Artificial Intelligence & Machine Learning

---

## 📄 License

This project was developed as a Major Project for B.Tech (AI & ML) — Session 2025-26.
