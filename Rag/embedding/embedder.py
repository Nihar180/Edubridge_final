from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text):
        return self.model.encode(text).tolist()

    def embed_documents(self, documents):
        return self.model.encode(documents).tolist()


if __name__ == "__main__":
    embedder = Embedder()

    text = "Photosynthesis is the process by which green plants make their food."

    embedding = embedder.embed_text(text)

    print("Embedding generated successfully!")
    print("Number of dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])