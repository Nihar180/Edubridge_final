from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline.pipeline import RAGPipeline


app = FastAPI(
    title="EduBridge AI Tutor API",
    description="RAG-powered AI Tutor API",
    version="1.0.0"
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
