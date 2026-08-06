import pandas as pd


def convert_csv_to_xls(csv_file_path, xls_file_path): 
    
    df = pd.read_csv(csv_file_path, encoding='latin1', sep=';') 
    df.to_excel(xls_file_path, index=False) 