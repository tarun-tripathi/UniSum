# MultiSourceRAG API - Manual Testing Guide

## 🔧 Setup
Server is running at: **http://localhost:8000**

---

## Method 1: Browser (Simplest)

### Test 1: Welcome Endpoint
```
Open in browser: http://localhost:8000/
```
**Expected:** `{"message":"WELCOME TO MULTI-SOURCE RAG APPLICATION"}`

### Test 2: Swagger UI (Interactive Docs)
```
Open in browser: http://localhost:8000/docs
```
This opens an interactive API documentation where you can test all endpoints!

### Test 3: ReDoc (Alternative Docs)
```
Open in browser: http://localhost:8000/redoc
```

---

## Method 2: Terminal (curl commands)

### Test 1: GET / (Welcome)
```bash
curl http://localhost:8000/
```

### Test 2: POST /web-rag (Load Website)
```bash
curl -X POST http://localhost:8000/web-rag \
  -H "Content-Type: application/json" \
  -d '{
    "web_url": "https://example.com"
  }'
```

**Response Example:**
```json
{
  "message": "uuid-collection-name"
}
```
Save this collection ID for next test!

### Test 3: POST /web-query (Query Website)
```bash
curl -X POST http://localhost:8000/web-query \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "your-collection-id-here",
    "question": "What is this website about?"
  }'
```

### Test 4: POST /upload-pdf (Upload PDF)
```bash
curl -X POST -F "file=@/path/to/your/file.pdf" http://localhost:8000/upload-pdf
```

**Response Example:**
```json
{
  "message": "uuid-collection-name"
}
```

### Test 5: POST /pdf-rag (Query PDF)
```bash
curl -X POST http://localhost:8000/pdf-rag \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "your-pdf-collection-id",
    "question": "What is the main topic?"
  }'
```

---

## Method 3: Visual Tools (Recommended for Beginners)

### Using Insomnia or Postman

**Download:**
- Insomnia: https://insomnia.rest/
- Postman: https://www.postman.com/

**Steps:**
1. Open the app
2. Create new HTTP request
3. Select method (GET/POST)
4. Enter URL: `http://localhost:8000/endpoint`
5. For POST: Go to Body → select JSON → paste your JSON
6. Click Send

**Example for /web-rag in Postman:**
```
METHOD: POST
URL: http://localhost:8000/web-rag
BODY (JSON):
{
  "web_url": "https://example.com"
}
```

---

## Method 4: Python Script (Advanced)

Create `test_manual.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Welcome
print("1️⃣ Testing GET /")
response = requests.get(f"{BASE_URL}/")
print(response.json())
print()

# Test 2: Load website
print("2️⃣ Testing POST /web-rag")
response = requests.post(
    f"{BASE_URL}/web-rag",
    json={"web_url": "https://example.com"}
)
result = response.json()
print(result)
collection_id = result.get("message")
print()

# Test 3: Query website
print("3️⃣ Testing POST /web-query")
response = requests.post(
    f"{BASE_URL}/web-query",
    json={
        "collection_name": collection_id,
        "question": "What is this website?"
    }
)
print(response.json())
print()

# Test 4: Upload and query PDF
print("4️⃣ Testing POST /upload-pdf")
with open("/tmp/python_guide.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/upload-pdf", files=files)
    pdf_collection = response.json().get("message")
    print(response.json())
print()

print("5️⃣ Testing POST /pdf-rag")
response = requests.post(
    f"{BASE_URL}/pdf-rag",
    json={
        "collection_name": pdf_collection,
        "question": "What are key features?"
    }
)
print(response.json())
```

Run with:
```bash
cd /Users/taruntripathi/Downloads/MultiSourceRAG/MultiSourceRAG
source env/bin/activate
pip install requests
python test_manual.py
```

---

## Test Workflows

### Workflow 1: Website RAG (Fastest)
```
1. Load website  → /web-rag
   ↓ Get collection_id
2. Ask question → /web-query
   ↓ Get answer
```

### Workflow 2: PDF RAG
```
1. Upload PDF    → /upload-pdf
   ↓ Get collection_id
2. Ask question  → /pdf-rag
   ↓ Get answer
```

---

## Example Test Scenarios

### Scenario 1: Learn about Python
```bash
# Upload PDF about Python
curl -X POST -F "file=@python_guide.pdf" http://localhost:8000/upload-pdf

# Get collection ID from response
# e.g., "9d469a0b-d8e9-493f-8c7f-1016d83c3f1acollection"

# Ask questions
curl -X POST http://localhost:8000/pdf-rag \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "9d469a0b-d8e9-493f-8c7f-1016d83c3f1acollection",
    "question": "What programming languages does Python compete with?"
  }'
```

### Scenario 2: Research from Website
```bash
# Load documentation website
curl -X POST http://localhost:8000/web-rag \
  -H "Content-Type: application/json" \
  -d '{"web_url": "https://python.org"}'

# Get collection ID, then ask
curl -X POST http://localhost:8000/web-query \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "returned-collection-id",
    "question": "How do I install Python?"
  }'
```

---

## Check Server Status

```bash
# Is server running?
curl -I http://localhost:8000/

# Expected response:
# HTTP/1.1 200 OK
```

---

## Terminal Shortcuts for Easy Testing

```bash
# Save this as test_shortcuts.sh
alias test-welcome="curl http://localhost:8000/"

test_web() {
  curl -X POST http://localhost:8000/web-rag \
    -H "Content-Type: application/json" \
    -d "{\"web_url\": \"$1\"}"
}

test_question() {
  curl -X POST http://localhost:8000/web-query \
    -H "Content-Type: application/json" \
    -d "{\"collection_name\": \"$1\", \"question\": \"$2\"}"
}

# Usage:
# test-welcome
# test_web "https://example.com"
# test_question "collection-id" "Your question here"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Server not running. Start with: `python main.py` |
| "Cannot GET /" | Wrong URL. Use `http://localhost:8000/` |
| JSON parse error | Check JSON syntax in -d parameter |
| 404 Not Found | Endpoint doesn't exist. Check spelling |
| Timeout | LLM model loading. Wait 30-60 seconds |

---

## Watch Server Logs

Keep terminal with server open to see:
- Incoming requests
- Processing status
- Generated answers
- Errors (if any)

