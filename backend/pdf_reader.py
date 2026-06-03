from pypdf import PdfReader

def read_pdf(pdf_path):

    text = ""

    pdf_reader = PdfReader(pdf_path)

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text