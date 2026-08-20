# RAG + AI Chatbot

This folder contains the RAG pipeline and AI doubt solver for the EduBridge AI Tutor project.

## Responsibilities

- Educational document ingestion
- Text chunking
- Embeddings
- Vector database
- Retrieval
- LLM integration
- RAG pipeline
- AI doubt solver

## Run the AI service

From this directory, install the dependencies and configure the existing Groq provider:

```powershell
pip install -r requirements.txt
$env:GROQ_API_KEY = "your-groq-api-key"
uvicorn api:app --host 127.0.0.1 --port 8001
```

The frontend calls `POST http://127.0.0.1:8001/ask` with JSON fields `question`,
`class_name`, and `subject`. Add source documents under `data/documents`, then
run the existing vector-store ingestion before asking document-grounded questions.