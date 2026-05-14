from parser import parser, filter_transactions
from src import Transaction, ClassTransaction
from wrangler import load_dataframe, convert_dtypes
import os 

# Introduction
print('Welcome to the Python app!')

# Assign file path for the processed .csv file
pro_path = r"C:\Users\hp\Desktop\Restart\POS Profit Calculator\data\processed\output.csv"

#       PARSING, FILTERING & WRANGLING OF DATA
# Check if file already exists to avoid redundant processing
if os.path.exists(pro_path) is False:
    # Receive file path input from the user and remove any surrounding quotes from input
    file_path = input('Enter the file path for the bank statement: \n')
    file_path = file_path.strip('"')
    # Processing & Parsing the PDF file, filtering transactions and saving to .csv file
    v1 = parser(file_path)
    filter_transactions(v1)
    print('Transactions have been filtered and saved to output.csv')
else:
    pass

#       LOADING DATA INTO A DATAFRAME, WRANGLING DATA
# Load the processed .csv file into a DataFrame and convert data types
main = load_dataframe(pro_path)
main = convert_dtypes(main)

#       MAKE EACH TRANSACTION AN OBJECT OF THE CLASS TRANSACTION AND PERFORMING OPERATIONS ON THE OBJECTS
transaction = [Transaction(*row) for row in main.itertuples(index = False)]
class_txt = []
for row in transaction:
    class_txt.append(row.classification())
# Add the classifications to the DataFrame as a new column
main['Transaction_Type'] = class_txt

#       CALCULATE PROFIT PER TRANSACTION & OPERATOR CHARGE
# Profit per transaction
transaction = [ClassTransaction(*row) for row in main.itertuples(index = False)]
profit_txt = []
operator_charge = []
for row in transaction:
    profit_txt.append(row.agent_charge())

# Service charge by operator
for row in transaction:
    operator_charge.append(row.service_charge())

#       CALCULATE TOTAL PROFIT
# Agent fee
fee = sum(profit_txt)
print(f'You charged fees totalling: {fee}')

# Operator charge
charge = sum(operator_charge)
print(f'You were charged: {charge}')

# Total Profit
profit = fee - charge
print(f'Profit for the day: {profit}')