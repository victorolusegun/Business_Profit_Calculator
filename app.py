from parser import parser

print('Welcome to the Python app!')
file_path = input('Enter the bank statement: \n')
file_path = file_path.strip('"')  # Remove any surrounding quotes from the input
parser(file_path)