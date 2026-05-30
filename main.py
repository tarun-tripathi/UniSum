from dotenv import load_dotenv
from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel,Field

from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.document_loaders import WebBaseLoader
# from fastapi.responses import StreamingResponse
# from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from langchain_core.documents import Document

# from langchain.schema import Document
from langchain_chroma import Chroma
import fitz
import os
load_dotenv()
hf_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# from docx import Document   # for Word documents
# from pptx import Presentation  # for PowerPoint files

import uuid
# from langchain_unstructured import UnstructuredLoader

from typing import Annotated
import shutil
app=FastAPI()
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    
llm_endpoint = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-R1-0528",
        task="text-generation",
        huggingfacehub_api_token=hf_api_key
        )

chat_model = ChatHuggingFace(llm=llm_endpoint)

prompt = PromptTemplate(
    template="""
You are an assistant that must answer ONLY using the information in the provided context.

Rules:
- If the answer exists in the context: respond in short, accurate form in 50 words.
- If the answer is NOT in the context: respond exactly with "no".
- Do NOT repeat context.
- Do NOT add explanations.
- Do NOT guess.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)

@app.get("/")
def home():
    return {"message":"WELCOME TO MULTI-SOURCE RAG APPLICATION"}

# @app.post("/webRag")
# def webBasedRag(req:WebRagRequest):
#     return {"url":req.url, "questions":req.questions}

# # @app.post("/upload")
# # async def uploadFile(file:UploadFile):
# #     content=await file.read()
# #     # return content
# #     return StreamingResponse(BytesIO(content), media_type=file.content_type)

print("----------------------------------------------------------------------------------------------------------------------------")
print('----------------------------------------------------------------------------------------------------------------------------')

import re

def clean_response(text: str) -> str:
    # Remove <think> ... </think> blocks (multi-line safe)
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned.strip()


print("--------------------------------------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------------------------------------")


class PdfRagRequest(BaseModel):
    collection_name:Annotated[str,Field(..., title="The name of collection where vectors are stored",description="For pdf based rag application",examples=["uuidcollection"])]
    question:Annotated[str,Field(...)]

@app.post("/upload-pdf")
def upload_pdf(file:UploadFile=File(...)):
    filename=file.filename
    path=f"uploads/{filename}"
    with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    pages = fitz.open(path)
    docs=[]
    for page in pages:
       doc= Document(page_content=page.get_text())
       docs.append(doc)

    pages.close()
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450, chunk_overlap=50, separators= separators 
    # 256-512 with overlap 10-25% default 512 tokens and 128 overlap
        )
    splits = text_splitter.split_documents(docs)
    print("The number of chunks are:")
    print(len(splits))
    print("---------------------------------------")
    
 
    collection_name= str(uuid.uuid4())+"collection"
    vector_store=Chroma(
            embedding_function=embedding_model,
            persist_directory='chroma_db',
            collection_name=collection_name
        )
    ids=vector_store.add_documents(splits)
    print("The ids stored in vector store Chroma are:")
    print(ids)
    print(len(ids))
    print("----------------------------------------------------------")

    return {"message":collection_name}

@app.post("/pdf-rag")
def pdfRAG(postBody:PdfRagRequest):
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_store=Chroma(
            embedding_function=embedding_model,
            persist_directory='chroma_db',
            collection_name= postBody.collection_name
        )
        retriever=vector_store.as_retriever(search_kwargs={"k":5})
        retrived_docs=retriever.invoke(postBody.question)

        context=""

        for doc in retrived_docs:
            context+=doc.page_content
        
        message=prompt.invoke({"context":context,"question":postBody.question})
        output=chat_model.invoke(message)
        print("The fetched chunks from vector stor most related to query")
        print("-----------------------------------------------------------------------")
        print(context)
        print("----------------------------------------------------------------------")
        print("The final output as given by llm model")
        print("-------------------------------------------------------------")
        print(output.content)
        print("----------------------------------------------")
        print("Successfully Executed")
        print("--------------------------------------------")
        return {"message":clean_response(output.content)}


# --------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

class WebRagRequest1(BaseModel):
    web_url:Annotated[str,Field(..., title="The url of any static html website",description="For rag based application using WebBaseLoader",examples=["www.example1.com"])]

@app.post("/web-rag")

def web_rag_app(postBody:WebRagRequest1):
    loader = WebBaseLoader(postBody.web_url)
    pages = []
    for doc in loader.lazy_load():
       pages.append(doc)

    pages = filter_complex_metadata(pages)
    separators=[
        "\n\n",
        "\n",
        ".",
        # " ",
        ""
    ]
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450, chunk_overlap=50, separators= separators 
    # 256-512 with overlap 10-25% default 512 tokens and 128 overlap
        )
    splits = text_splitter.split_documents(pages)
    print("-------------------------------------")
    print("No. of chunks created")
    print("--------------------------")
    print(len(splits))
    embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    collection_name= str(uuid.uuid4())+"collection"
    vector_store=Chroma(
            embedding_function=embedding_model,
            persist_directory='chroma_db',
            collection_name= collection_name
    )
    ids=vector_store.add_documents(splits)
    print("No. of ids created=no of chunks stored in chroma vector store")
    print("-------------------------------------------------------------------------------")
    print(ids)
    print(len(ids))
        
    return {"message":collection_name}

class WebRagRequest2(BaseModel):
    collection_name:Annotated[str,Field(..., title="The name of collection where vectors are stored",description="For web based rag application",examples=["uuidcollection"])]
    question:Annotated[str,Field(...)]

# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

@app.post("/web-query")

def webQueryRequest(postBody:WebRagRequest2):
    
    vector_store=Chroma(
            embedding_function=embedding_model,
            persist_directory='chroma_db',
            collection_name= postBody.collection_name
    )
    retriever=vector_store.as_retriever(search_kwargs={"k":10})
    docs=retriever.invoke(postBody.question)

    retrieved_text=""
    for doc in docs:
            retrieved_text+=doc.page_content
    message=prompt.invoke({"context":retrieved_text,"question":postBody.question})
    output=chat_model.invoke(message)
    print("The fetched chunks from vector stor most related to query")
    print("-----------------------------------------------------------------------")
    print(retrieved_text)
    print("----------------------------------------------------------------------")
    print("The final output as given by llm model")
    print("-------------------------------------------------------------")
    print(output.content)
    print("----------------------------------------------")
    print("Successfully Executed")
    print("--------------------------------------------")
    return {"message":clean_response(output.content)}




# --------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
