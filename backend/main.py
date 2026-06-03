from fastapi import FastAPI, UploadFile, File
from backend.pdf_reader import read_pdf
from backend.text_chunker import get_text_chunks
from backend.vector_store import store_vectors
from backend.query import ask_question
from backend.utils import create_folder

import shutil
import traceback

app = FastAPI(
    title="AI DevOps RAG Assistant",
    description="Enterprise AI-powered document intelligence system",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"

create_folder(UPLOAD_FOLDER)


@app.get("/")
def home():

    return {
        "message": "AI DevOps RAG Assistant Running"
    }


@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...)):

    try:

        file_path = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # READ PDF
        text = read_pdf(file_path)

        # SPLIT TEXT
        chunks = get_text_chunks(text)

        # STORE IN VECTOR DB
        store_vectors(chunks)

        return {
            "status": "success",
            "message": "PDF uploaded and processed successfully",
            "file_name": file.filename,
            "chunks_created": len(chunks)
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/chat")
def chat(query: str):

    try:

        answer = ask_question(query)

        return {
            "status": "success",
            "question": query,
            "answer": answer
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "status": "error",
            "error": str(e)
        }