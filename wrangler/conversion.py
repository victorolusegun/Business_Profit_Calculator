import pandas as pd

def convert_dtypes(df):
    df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
    df['Time'] = pd.to_datetime(df['Time'], errors = 'coerce')
    df['Reference ID'] = df['Reference ID'].astype(str)
    return df