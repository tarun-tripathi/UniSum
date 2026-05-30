#!/bin/bash

# Create a sample PDF for testing
echo "Creating sample PDF for testing..."

python3 << 'EOF'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create a sample PDF
pdf_path = "/tmp/sample_document.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)
c.drawString(100, 750, "Sample Document for RAG Testing")
c.drawString(100, 730, "")
c.drawString(100, 710, "Python Programming Language")
c.drawString(100, 690, "Python is a high-level, interpreted programming language known for its")
c.drawString(100, 670, "simplicity and readability. It was created by Guido van Rossum and first")
c.drawString(100, 650, "released in 1991.")
c.drawString(100, 630, "")
c.drawString(100, 610, "Key Features of Python:")
c.drawString(100, 590, "1. Easy to learn and understand")
c.drawString(100, 570, "2. Supports multiple programming paradigms")
c.drawString(100, 550, "3. Large standard library")
c.drawString(100, 530, "4. Cross-platform compatibility")
c.drawString(100, 510, "5. Active community support")
c.drawString(100, 490, "")
c.drawString(100, 470, "Common Applications:")
c.drawString(100, 450, "- Web Development (Django, Flask)")
c.drawString(100, 430, "- Data Science (Pandas, NumPy)")
c.drawString(100, 410, "- Machine Learning (TensorFlow, PyTorch)")
c.drawString(100, 390, "- Automation (Scripts, Bots)")
c.drawString(100, 370, "- Scientific Computing")
c.save()

print(f"✅ Sample PDF created: {pdf_path}")
EOF

echo ""
echo "Now testing PDF upload..."
echo ""

# Upload PDF
echo "📌 Uploading PDF to /upload-pdf..."
UPLOAD_RESPONSE=$(curl -s -X POST -F "file=@/tmp/sample_document.pdf" http://localhost:8000/upload-pdf)
COLLECTION_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.message' 2>/dev/null)

echo "Upload Response:"
echo "$UPLOAD_RESPONSE" | jq .
echo ""
echo "Extracted Collection ID: $COLLECTION_ID"
echo ""

# Query the PDF
if [ "$COLLECTION_ID" != "null" ] && [ ! -z "$COLLECTION_ID" ]; then
    echo "📌 Querying PDF with question..."
    echo ""
    curl -s -X POST http://localhost:8000/pdf-rag \
      -H "Content-Type: application/json" \
      -d "{\"collection_name\":\"$COLLECTION_ID\",\"question\":\"What are the key features of Python?\"}" | jq .
else
    echo "❌ Could not extract collection ID from upload response"
fi
