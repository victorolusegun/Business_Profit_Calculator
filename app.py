import pdfplumber
from src import *

print('Welcome to the Python app!')

with pdfplumber.open("C:\\Users\\hp\\Desktop\\Restart\\POS Profit Calculator\\data\\raw\\Daily_Statement.pdf") as pdf:
    for page in pdf.pages:
        table = page[0].extract_text().split()
        print(table)