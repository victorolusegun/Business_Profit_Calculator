import pdfplumber

def ppay_parser(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = []
        for page in pdf.pages:
            table = page.extract_text()
            pages.append(table)
        return pages