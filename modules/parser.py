"""
parser.py
---------
Extracts raw text from uploaded PDF resumes using PyPDF2.

HOW IT WORKS:
    1. Streamlit passes the uploaded file as a file-like object
    2. PyPDF2 reads each page and extracts the text layer
    3. All pages are joined into one clean string

LIMITATION TO KNOW FOR INTERVIEWS:
    This only works on text-based PDFs.
    Scanned/image PDFs return empty text and need OCR (e.g. Tesseract).
    That is a great future improvement to mention in your presentation.
"""

import PyPDF2


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from an uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object (behaves like a file)

    Returns:
        str: All extracted text as one string, or "" on failure
    """
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()

            # Some pages return None — guard against it
            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"[parser.py] Error reading PDF: {e}")
        return ""

    # Collapse multiple spaces/newlines into single spaces
    text = " ".join(text.split())
    return text


def get_word_count(text: str) -> int:
    """Returns the number of words in a text string."""
    return len(text.split()) if text else 0