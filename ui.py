from datetime import datetime
import streamlit as st
from op_parser import ppay_parser, filter_txn
from src import Transaction, Class_Transaction
from wrangler import *

#               APP CONFIGURATION
st.set_page_config(page_title='POS Profit Calculator', page_icon=':money_with_wings:')

#               SESSION STATE VARIABLES
if 'txn_state' not in st.session_state:
    st.session_state['txn_state'] = False
if 'file_path' not in st.session_state:
    st.session_state['file_path'] = None
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = None
if 'working_df' not in st.session_state:
    st.session_state['working_df'] = None
if 'calc_df' not in st.session_state:
    st.session_state['calc_df'] = None
if 'calc_started' not in st.session_state:
    st.session_state['calc_started'] = False

#               HEADER
st.write('# Agent Profit_Calc')

#               FILE UPLOAD, DATA PREP AND DISPLAY
if st.session_state['txn_state'] is False:
    file_path = st.file_uploader('Upload your account statement for today (PDF format only)', type='pdf')
    st.session_state['file_path'] = file_path
if st.button('Generate Transaction List'):
    st.session_state['txn_state'] = True
if st.session_state['txn_state'] is True:
    if st.session_state['file_path'] is not None:
        v1 = ppay_parser(st.session_state['file_path'])
        filtered_transactions = filter_txn(v1)
        main = dataframe(filtered_transactions)
        main = convert_dtypes(main)
        st.session_state['main_df'] = main
        st.session_state['working_df'] = main
        st.write(st.session_state['main_df'])
if st.session_state['file_path'] is None:
    st.write('Please upload a file to generate the transaction list.')

#               TRANSACTIONS BEING OBJECTS OF CLASSES
if st.session_state['working_df'] is not None:
    transactions = [Transaction(*row) for row in st.session_state['working_df'].itertuples(index = False)]
    class_txt = []
    for row in transactions:
        class_txt.append(row.classification())
    st.session_state['working_df']['txn_type'] = class_txt
    st.session_state['calc_df'] = st.session_state['working_df']

#               FILTERING OUT UNCHARGED TRANSACTIONS WITH USER ASSISTANCE
st.write('### Verify Uncharged Transactions')
option = st.radio('Are there any uncharged transactions in the list above?', ('Yes', 'No'))
if option == 'Yes' and st.session_state['calc_df'] is not None:
    chosen_time = st.selectbox('Select the time period the uncharged transaction occured:', [x for x in range(24)])
    if chosen_time is not None:
        st.write(st.session_state['calc_df'][st.session_state['calc_df']['Time'].apply(lambda t: t.hour == chosen_time)])
        pot_uncharged_txn = [i for i in st.session_state['calc_df'][st.session_state['calc_df']['Time'].apply(lambda t: t.hour == chosen_time)].index]
        uncharged_txn = st.multiselect('Select the uncharged transactions:', pot_uncharged_txn)
        if uncharged_txn:
            st.session_state['calc_df'] = st.session_state['working_df'].drop(index = uncharged_txn)
    st.write('Click the button below to proceed')
    if st.button('Start Calculations'):
        st.session_state['calc_started'] = True
elif option == 'No' and st.session_state['calc_df'] is not None:
    st.session_state['calc_df'] = st.session_state['main_df'].copy()
    st.session_state['calc_started'] = True


#               CALCULATIONS
if st.session_state['calc_df'] is not None:
    calc_transactions = [Class_Transaction(*row) for row in st.session_state['calc_df'].itertuples(index = False)]
    profit_txt = []
    operator_charge = []
    for row in calc_transactions:
        profit_txt.append(row.agent_charge())
# Service charge by operator
    for row in calc_transactions:
        operator_charge.append(row.service_charge())
# Calculations
    agent_profit = sum(profit_txt)
    operator_fee = sum(operator_charge)
    profit = agent_profit - operator_fee

#               DISPLAY CALCULATIONS
if st.session_state['calc_started'] is True:
    st.write('### Calculations')
# Amount you charged customer
    if st.button('Show Agent Fee'):
        st.write(f'Agent Profit: ₦{agent_profit:.2f}')
# Amount the operator charged you
    if st.button('Show Operator Fee'):
        st.write(f'Operator Fee: ₦{operator_fee:.2f}')
# Net profit
    if st.button('Show Net Profit'):
        st.write(f'Net Profit: ₦{profit:.2f}')