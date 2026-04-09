from parser import *
from wrangler import *

print('Welcome to the Python app!')
file_path = input('Enter the file path for the bank statement: \n')
file_path = file_path.strip('"')  # Remove any surrounding quotes from the input
v1 = parser(file_path)
filter_transactions(v1)
print('Transactions have been filtered and saved to output.csv')
pro_path = r"C:\Users\hp\Desktop\Restart\POS Profit Calculator\data\processed\output.csv"
main = load_dataframe(pro_path)
print(main.head())
main = convert_dtypes(main)
main.info()