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
    print('Parsing and filtering successful')
else:
    pass

#       LOADING DATA INTO A DATAFRAME, WRANGLING DATA
# Load the processed .csv file into a DataFrame and convert data types
main = load_dataframe(pro_path)
main = convert_dtypes(main)

#       MAKE EACH TRANSACTION AN OBJECT OF THE CLASS TRANSACTION AND PERFORMING OPERATIONS ON THE OBJECTS
transaction = [Transaction(*row) for row in main.itertuples(index = False)]
class_txt = []
rnd_amt = []
for row in transaction:
    class_txt.append(row.classification())
# Add the classifications to the DataFrame as a new column
main['Transaction_Type'] = class_txt

#       ROUNDING AMOUNT TO AID ESTIMATION
for row in transaction:
    rnd_amt.append(row.rounding())
# Add to DataFrame (main)
main['rnd_amt'] = rnd_amt
#       VERIFY CHARGED TRANSACTIONS THROUGH USER INPUT
# Initialise list containing available responses and variable to store user input
response = ['yes', 'no']
num_charged = ''
# Receive user input and loop until valid response is received. User can exit by typing 'exit
while num_charged not in response:
    print('Answer YES or NO to proceed or enter EXIT to quit the app')
    num_charged = input('Would you like to verify the transactions you charged fees for? \n')
    num_charged = num_charged.lower()
    if num_charged == 'exit':
        print('Exiting application......')
        exit()
# If user answers yes, receive input for the amount of the transaction not charged and display the transactions that match the input amount. If user answers no, skip to profit calculation.
if num_charged == 'yes':
    while True:
        try:
            price = input('Input amount of transaction not charged: \n')
            price = float(price)
            neg_price = -1 * price
            break
        except ValueError:
            print('Invalid input. Please enter a valid number.')
        if price.lower() == 'exit':
            print('Exiting application......')
            exit()
# Query the DataFrame for transactions matching the input amount and display the relevant information. If no transactions are found, prompt user to check input and try again.
    tx_samples = main.query('rnd_amt == @price or rnd_amt == @neg_price')
    if len(tx_samples) != 0:
        vis_samples = tx_samples[['Date', 'Time', 'Amount', 'Transaction_Type']]
        print(vis_samples.head(len(vis_samples)))
    else:
        print('No transactions found matching that amount. Please check your input and try again or enter END to proceed.')
else:
    pass

#       CALCULATIONS
# Profit per transaction
transaction = [ClassTransaction(*row) for row in main.itertuples(index = False)]
profit_txt = []
operator_charge = []
for row in transaction:
    profit_txt.append(row.agent_charge())

# Service charge by operator
for row in transaction:
    operator_charge.append(row.service_charge())

# Agent fee
fee = sum(profit_txt)
print(f'You charged fees totalling: {fee}')

# Operator charge
charge = sum(operator_charge)
print(f'You were charged: {charge}')

# Total Profit
profit = fee - charge
print(f'Profit for the day: {profit}')