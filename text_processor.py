from PyPDF2 import PdfReader

def read_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=10000):
    """Breaks down massive text bodies into smaller, rate-limit friendly blocks"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
