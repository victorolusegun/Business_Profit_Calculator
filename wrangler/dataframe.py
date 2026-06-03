import pandas as pd

def dataframe(df):
    df = pd.DataFrame(df, columns=['Date', 'Time', 'Reference ID', 'Amount', 'Balance'])
    return df