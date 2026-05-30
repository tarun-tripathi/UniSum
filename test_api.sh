#!/bin/bash

echo "=========================================="
echo "🚀 MULTI-SOURCE RAG API TEST SUITE"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Home endpoint
echo "📌 TEST 1: GET / (Welcome Endpoint)"
echo "==========================================="
curl -X GET "$BASE_URL/" | jq .
echo -e "\n✅ Test 1 Complete\n"
sleep 2

# Test 2: Create a sample PDF for testing
echo "📌 TEST 2: POST /upload-pdf (PDF Upload)"
echo "==========================================="
# Create a simple text file to test (since we don't have a real PDF)
echo "Python is a programming language. It was created by Guido van Rossum. Python is used for web development, data science, and automation." > /tmp/test_doc.txt

# Try uploading - note: endpoint expects PDF but we'll see what happens
echo "Creating sample PDF for upload..."
# For now, we'll just show the curl command
echo "curl -X POST -F 'file=@/path/to/document.pdf' $BASE_URL/upload-pdf"
echo "Note: Replace '/path/to/document.pdf' with your actual PDF file"
echo -e "\n⏭️  Skipping actual PDF upload (need real PDF file)\n"
sleep 2

# Test 3: Web RAG - Load from website
echo "📌 TEST 3: POST /web-rag (Load Website Content)"
echo "==========================================="
echo "Loading content from example.com..."
WEB_RESPONSE=$(curl -s -X POST "$BASE_URL/web-rag" \
  -H "Content-Type: application/json" \
  -d '{"web_url":"https://example.com"}')

COLLECTION_ID=$(echo "$WEB_RESPONSE" | jq -r '.message' 2>/dev/null)
echo "Response: $WEB_RESPONSE" | jq .
echo "Collection ID: $COLLECTION_ID"
echo -e "\n✅ Test 3 Complete\n"
sleep 2

# Test 4: Web Query - Ask question about website
if [ "$COLLECTION_ID" != "null" ] && [ ! -z "$COLLECTION_ID" ]; then
  echo "📌 TEST 4: POST /web-query (Query Website Content)"
  echo "==========================================="
  echo "Asking question about the website..."
  curl -s -X POST "$BASE_URL/web-query" \
    -H "Content-Type: application/json" \
    -d "{\"collection_name\":\"$COLLECTION_ID\",\"question\":\"What is this website about?\"}" | jq .
  echo -e "\n✅ Test 4 Complete\n"
else
  echo "⚠️  Skipping Test 4 - No valid collection ID from previous test\n"
fi

# Additional test information
echo "=========================================="
echo "📖 API ENDPOINTS SUMMARY"
echo "=========================================="
echo ""
echo "1️⃣  GET  / → Welcome message"
echo ""
echo "2️⃣  POST /upload-pdf → Upload PDF"
echo "   • Accepts: file (multipart/form-data)"
echo "   • Returns: {\"message\": \"collection_name\"}"
echo ""
echo "3️⃣  POST /pdf-rag → Query PDF"
echo "   • Body: {\"collection_name\": \"xxx\", \"question\": \"xxx\"}"
echo "   • Returns: {\"message\": \"answer\"}"
echo ""
echo "4️⃣  POST /web-rag → Load Website"
echo "   • Body: {\"web_url\": \"https://example.com\"}"
echo "   • Returns: {\"message\": \"collection_name\"}"
echo ""
echo "5️⃣  POST /web-query → Query Website"
echo "   • Body: {\"collection_name\": \"xxx\", \"question\": \"xxx\"}"
echo "   • Returns: {\"message\": \"answer\"}"
echo ""
echo "=========================================="
echo "✅ ALL TESTS COMPLETED!"
echo "=========================================="
