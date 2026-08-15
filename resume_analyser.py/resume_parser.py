"""
src/resume_parser.py
Extracts raw text from uploaded PDF and DOCX files.
"""

from typing import Union
import io
import pypdf
import docx


def extract_text_from_pdf(file_source: Union[str, io.BytesIO]) -> str:
    """
    Extracts text page-by-page from a PDF file path or file stream.
    """
    text_content = []
    try:
        reader = pypdf.PdfReader(file_source)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        return "\n".join(text_content)
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {str(e)}") from e


def extract_text_from_docx(file_source: Union[str, io.BytesIO]) -> str:
    """
    Extracts text paragraph-by-paragraph from a DOCX file path or file stream.
    """
    try:
        doc = docx.Document(file_source)
        text_content = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(text_content)
    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX: {str(e)}") from e


def parse_resume(file_source: Union[str, io.BytesIO], file_type: str) -> str:
    """
    Dispatches file to the appropriate parser based on extension.
    """
    normalized_type = file_type.lower().strip().replace(".", "")
    if normalized_type == "pdf":
        return extract_text_from_pdf(file_source)
    elif normalized_type in ["docx", "doc"]:
        return extract_text_from_docx(file_source)
    else:
        raise ValueError(f"Unsupported file format: {file_type}. Supported: PDF, DOCX")