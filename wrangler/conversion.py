import pandas as pd

def convert_dtypes(df):
    df['Date'] = pd.to_datetime(df['Date'], format = '%Y/%m/%d', errors = 'coerce')
    df['Time'] = pd.to_datetime(df['Time'], format = '%H:%M:%S', errors = 'coerce')
    df['Reference ID'] = df['Reference ID'].astype(str)
    return df