from parser import parser, filter_transactions
from wrangler import load_dataframe, convert_dtypes
import os 

# Introduction
print('Welcome to the Python app!')

# Assign file path for the processed .csv file
pro_path = r"C:\Users\hp\Desktop\Restart\POS Profit Calculator\data\processed\output.csv"

if os.path.exists(pro_path) is False:
# Receive file path input from the user and remove any surrounding quotes from input
    file_path = input('Enter the file path for the bank statement: \n')
    file_path = file_path.strip('"')

    # Processing the PDF file, filtering transactions and saving to .csv file
    v1 = parser(file_path)
    filter_transactions(v1)
    print('Transactions have been filtered and saved to output.csv')

    # Load the processed .csv file into a DataFrame and convert data types
    main = load_dataframe(pro_path)
    main = convert_dtypes(main)
else:
    print("File already exists.")