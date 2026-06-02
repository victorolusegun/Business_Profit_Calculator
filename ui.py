from datetime import datetime
import os
import streamlit as st
from parser import *
from src import Transaction, ClassTransaction
from wrangler import *

# Configuration of Application
st.set_page_config(page_title='POS Profit Calculator', page_icon=':money_with_wings:')

pro_path = r"C:\Users\hp\Desktop\Restart\POS Profit Calculator\data\processed\output.csv"

#       SESSION STATE VARIABLES
if 'txn_state' not in st.session_state:
    st.session_state['txn_state'] = False
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = None
if 'uncharged' not in st.session_state:
    st.session_state['uncharged'] = None
if 'charge' not in st.session_state:
    st.session_state['charge'] = None
if 'charged' not in st.session_state:
    st.session_state['charged'] = None
if 'profit' not in st.session_state:
    st.session_state['profit'] = None
if 'object' not in st.session_state:
    st.session_state['object'] = False
#      HEADER
st.write('# Agent Profit_Calc')

if os.path.exists(pro_path) is True:
    st.session_state['txn_state'] = True
    main = load_dataframe(pro_path)
    main = convert_dtypes(main)
    st.session_state['main_df'] = main
    st.write(main)
else:
    #      FILE UPLOAD & TRANSACTION LIST GENERATION
    if st.session_state['txn_state'] is False:
        file_path = st.file_uploader('Upload your account statement for today (PDF format only)', type='pdf')
    if st.button('Generate Transaction List'):
        st.session_state['txn_state'] = True
    if st.session_state['txn_state'] is True:
        try:
            v1 = parser(file_path)
            filter_transactions(v1)
            main = load_dataframe(pro_path)
            main = convert_dtypes(main)
            st.session_state['main_df'] = main
            st.write(main)
        except NameError:
            st.write('Please upload a file to generate the transaction list.')

#       FILTERING OUT UNCHARGED TRANSACTIONS WITH USER ASSISTANCE
st.write('### Verify Uncharged Transactions')
if st.button('YES'):
    st.session_state['uncharged'] = True
if st.button('NO'):
    st.session_state['uncharged'] = False

if st.session_state['uncharged'] is True:
    chosen_time = st.selectbox('Select the time period the uncharged transaction occured:', [x for x in range(24)])
    if chosen_time is not None:
        st.write(st.session_state['main_df'][st.session_state['main_df']['Time'].apply(lambda t: t.hour == chosen_time)])
        pot_uncharged_txn = [i for i in st.session_state['main_df'][st.session_state['main_df']['Time'].apply(lambda t: t.hour == chosen_time)].index ]
        uncharged_txn = st.multiselect('Select the uncharged transactions:', pot_uncharged_txn)
        if uncharged_txn:
            st.session_state['main_df'].drop(index = uncharged_txn, inplace = True)
        # st.write(st.session_state['main_df'])

    st.write('If there are multiple uncharged transactions, please select all that apply. If there are none, simply click the "Show Calculations" button below.')
    if st.button('Start Calculations'):
        st.session_state['uncharged'] = False

#        TRANSACTIONS BEING OBJECTS OF CLASSES
if st.session_state['main_df'] is not None and st.session_state['uncharged'] is False:
    transactions = [Transaction(*row) for row in st.session_state['main_df'].itertuples(index = False)]
    class_txt = []
    for row in transactions:
        class_txt.append(row.classification())
    st.session_state['main_df']['txn_type'] = class_txt
    st.session_state['object'] = True
    st.write(st.session_state['main_df'])

#       CALCULATIONS
if st.session_state['main_df'] is not None and st.session_state['object'] is True:
    transactions = [ClassTransaction(*row) for row in st.session_state['main_df'].itertuples(index = False)]
    profit_txt = []
    operator_charge = []
    for row in transactions:
        profit_txt.append(row.agent_charge())

    # Service charge by operator
    for row in transactions:
        operator_charge.append(row.service_charge())

    agent_profit = sum(profit_txt)
    operator_fee = sum(operator_charge)
    profit = agent_profit - operator_fee

#       DISPLAY CALCULATIONS
if st.session_state['uncharged'] is False:
    st.write('### Calculations')
    if st.button('Show Profit'):
        st.session_state['charge'] = agent_profit
        st.write(f'Agent Profit: ₦{agent_profit:.2f}')
    if st.button('Show Operator Fee'):
        st.session_state['charged'] = operator_fee
        st.write(f'Operator Fee: ₦{operator_fee:.2f}')
    if st.button('Show Net Profit'):
        st.session_state['profit'] = profit
        st.write(f'Net Profit: ₦{profit:.2f}')