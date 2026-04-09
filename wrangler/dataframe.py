import pandas as pd

def load_dataframe(file_path):
    data = pd.read_csv(file_path, header = None)
    data.columns = ['Date', 'Time', 'Reference ID', 'Amount', 'Balance']
    return data
