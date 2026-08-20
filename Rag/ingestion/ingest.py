from pathlib import Path
import json
import subprocess

from .loader import load_document
from .chunker import chunk_text

RAG_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = RAG_ROOT / "data" / "documents"
FRONTEND_CONTENT_BRIDGE = Path(__file__).with_name("frontend_content_bridge.mjs")

FRONTEND_CONTENT_METADATA = {
    "Mathematics-Algebra": {
        "class": "Grade 8",
        "subject": "Mathematics",
        "topic": "Algebra",
    },
}


def ingest_frontend_content():
    result = subprocess.run(
        ["node", str(FRONTEND_CONTENT_BRIDGE)],
        check=True,
        capture_output=True,
        text=True,
    )
    structured_content = json.loads(result.stdout)
    all_chunks = []

    for content_key, content in structured_content.items():
        metadata = FRONTEND_CONTENT_METADATA.get(content_key)
        if not metadata:
            continue

        text = "\n\n".join(
            [
                content["title"],
                f"Explanation:\n{content['explanation']}",
                "Examples:\n" + "\n".join(f"- {example}" for example in content["examples"]),
                "Key points:\n" + "\n".join(f"- {point}" for point in content["keyPoints"]),
            ]
        )

        for chunk in chunk_text(text):
            all_chunks.append(
                {
                    "text": chunk,
                    "source": "Frontend-mem1/src/data/learningContent.js",
                    "class": metadata["class"],
                    "subject": metadata["subject"],
                }
            )

    return all_chunks


def ingest_documents():
    all_chunks = ingest_frontend_content()

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