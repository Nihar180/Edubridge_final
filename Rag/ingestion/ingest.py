from pathlib import Path

from .loader import load_document
from .chunker import chunk_text

DOCUMENTS_DIR = Path("data/documents")


def ingest_documents():
    all_chunks = []

    pdf_files = list(DOCUMENTS_DIR.rglob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for file_path in pdf_files:
        print(f"\nProcessing: {file_path}")

        text = load_document(file_path)

        chunks = chunk_text(text)

        class_name = file_path.parent.name
        subject = file_path.stem.split("(")[-1].replace(")", "")

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": file_path.name,
                "class": class_name,
                "subject": subject
            })

        print(f"Created {len(chunks)} chunks.")

    return all_chunks


if __name__ == "__main__":
    chunks = ingest_documents()

    print("\n==============================")
    print(f"Total chunks created: {len(chunks)}")
    print("==============================")

    if chunks:
        print("\nExample chunk:")
        print(chunks[0]["text"])

        print("\nMetadata:")
        print(f"Source: {chunks[0]['source']}")
        print(f"Class: {chunks[0]['class']}")
        print(f"Subject: {chunks[0]['subject']}")