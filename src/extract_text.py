from pathlib import Path
from pypdf import PdfReader
from docx import Document

def read_pdf(file_path:str) -> str:
    """Extract text from a PDF file."""

    reader=PdfReader(file_path)
    text=""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()

def read_docx(file_path: str) -> str:
    """Extract text from a Docx file."""

    doc = Document(file_path)
    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )
    return text.strip()

def extract_text(file_path: str) -> str:
    """Automatically detect file type and extract text"""
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    if extension == ".docx":
        return read_docx(file_path)

    raise ValueError(f"Unsupported file type: {extension}")
