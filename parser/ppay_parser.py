import pdfplumber

def parser(file_path):
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_text()
            with open('output.csv', 'a') as pro:
                for line in table.split('\n'):
                    line_list = line.split()
                    pro.write(','.join(line_list) + '\n')
