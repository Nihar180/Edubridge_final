import chromadb
from embedding.embedder import Embedder


class Retriever:

    def __init__(self, top_k=5):
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_collection(
            name="edubridge_documents"
        )

        self.embedder = Embedder()
        self.top_k = top_k

    def retrieve(self, query, class_name=None, subject=None):

        query_embedding = self.embedder.embed_documents([query])[0]

        conditions = []

        if class_name:
            conditions.append({
                "class": class_name
            })

        if subject:
            conditions.append({
                "subject": subject
            })

        where = None

        if len(conditions) == 1:
            where = conditions[0]

        elif len(conditions) > 1:
            where = {
                "$and": conditions
            }

        if where:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=self.top_k,
                where=where
            )
        else:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=self.top_k
            )

        return results


if __name__ == "__main__":

    retriever = Retriever(top_k=5)

    query = input("\nAsk a question: ")

    class_name = input(
        "Enter class (example: class8) or press Enter: "
    ).strip()

    subject = input(
        "Enter subject (example: science) or press Enter: "
    ).strip()

    results = retriever.retrieve(
        query,
        class_name=class_name if class_name else None,
        subject=subject if subject else None
    )

    print("\n===== Retrieved Chunks =====\n")

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        print(f"--- Chunk {i + 1} ---")
        print(f"Source: {metadata['source']}")
        print(f"Class: {metadata['class']}")
        print(f"Subject: {metadata['subject']}")
        print(f"\n{document}\n")