"""
TODO: look several CV and add an optimization Layer
"""


import PyPDF2

def extract_keywords(pdf_file_path):
    text_keywords = ""
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            text_keywords += text
    return text_keywords.strip()

pdf_file_path = 'backend/tests/resume_Augustin_ROLET.pdf'
pdf_file_path = "backend/tests/CV Augustin ROLET - 2022.pdf"
text_keywords = extract_keywords(pdf_file_path)
print(text_keywords)
