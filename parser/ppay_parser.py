import pdfplumber

def parser(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = []
            for page in pdf.pages:
                table = page.extract_text()
                pages.append(table)
            return pages
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        quit()