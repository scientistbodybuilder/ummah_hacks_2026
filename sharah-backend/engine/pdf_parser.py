"""PDF text extraction utility."""

from __future__ import annotations

import fitz  # PyMuPDF


def parse_pdf_text(file_bytes: bytes) -> str:
    """
    Parse text content from a PDF file.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        
    Returns:
        Extracted text as a single string
        
    Raises:
        ValueError: If PDF cannot be parsed or is empty
    """
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to open PDF: {str(e)}")
    
    text_parts = []
    
    try:
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(text)
    finally:
        pdf_document.close()
    
    if not text_parts:
        raise ValueError("No text could be extracted from PDF. The file may be empty or contain only images.")
    
    return "\n\n".join(text_parts)
