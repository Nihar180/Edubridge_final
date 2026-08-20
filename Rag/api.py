import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_pipeline.pipeline import RAGPipeline


app = FastAPI(
    title="EduBridge AI Tutor API",
    description="RAG-powered AI Tutor API",
    version="1.0.0"
)


# Allow frontend to communicate with RAG API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create one RAG pipeline instance
rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str
    class_name: str
    subject: str


class QuestionResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "message": "EduBridge AI Tutor API is running"
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    answer = rag.answer(
        question=request.question,
        class_name=request.class_name,
        subject=request.subject
    )

    return {
        "answer": answer
    }