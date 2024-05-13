import PyPDF2


def extract_keywords(pdf_file_path: str) -> str:
    """
    Extracts keywords from a PDF file.

    Args:
        pdf_file_path (str): The file path of the PDF.

    Returns:
        str: A string containing extracted keywords.
    """
    text_keywords = ""
    with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            text_keywords += text
    return text_keywords.strip()


"""
# Example usage
pdf_file_path = "backend/tests/resume_Augustin_ROLET.pdf"
text_keywords = extract_keywords(pdf_file_path)
print(text_keywords)
"""
