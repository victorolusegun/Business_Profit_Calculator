import pdfplumber
from src import *

print('Welcome to the Python app!')
file_path = r"C:\\Users\\hp\\Desktop\\Restart\\POS Profit Calculator\\data\\raw\\Daily_Statement.pdf"
with pdfplumber.open(file_path) as pdf:
    page = pdf.pages[0]
    table = page.extract_text()
    for line in table.split('\n'):
        line_list = line.split()
        print(line_list)
    # print(table)
    # for page in pdf.pages:
    #     table = page.extract_text().split('\n')
    #     print(table)