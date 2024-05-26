import pypdf
import io


def extract_keywords_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts keywords from a PDF file given its bytes.

    Args:
        pdf_bytes (bytes): The bytes of the PDF file.

    Returns:
        str: A string containing extracted keywords.
    """
    text_keywords = ""
    pdf_file_like = io.BytesIO(pdf_bytes)
    pdf_reader = pypdf.PdfReader(pdf_file_like)
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:  # Check if text extraction was successful
            text_keywords += text
    return text_keywords.strip()
