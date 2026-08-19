from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_document(file_path):
    path = Path(file_path)

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    elif path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif path.suffix.lower() == ".docx":
        document = Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


if __name__ == "__main__":
    file_path = "data/documents/sample.txt"

    text = load_document(file_path)

    print("----- EXTRACTED TEXT -----")
    print(text)