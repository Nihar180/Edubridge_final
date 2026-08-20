import chromadb
from pathlib import Path
from ingestion.ingest import ingest_documents
from embedding.embedder import Embedder


RAG_ROOT = Path(__file__).resolve().parents[1]


class ChromaStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(RAG_ROOT / "data" / "chroma_db")
        )

        self.collection = self.client.get_or_create_collection(
            name="edubridge_documents"
        )

        self.embedder = Embedder()

    def add_documents(self, chunks, batch_size=100):
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]

            texts = [chunk["text"] for chunk in batch]

            embeddings = self.embedder.embed_documents(texts)

            ids = [
                f"chunk_{start + i}"
                for i in range(len(batch))
            ]

            metadatas = [
                {
                    "source": chunk["source"],
                    "class": chunk["class"],
                    "subject": chunk["subject"]
                }
                for chunk in batch
            ]

            self.collection.upsert(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )

            print(
                f"Stored {min(start + batch_size, len(chunks))}"
                f"/{len(chunks)} chunks"
            )


if __name__ == "__main__":
    chunks = ingest_documents()

    print(f"\nTotal chunks: {len(chunks)}")

    store = ChromaStore()
    store.add_documents(chunks)

    print("\nAll chunks stored successfully in ChromaDB!")