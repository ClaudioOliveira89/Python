import pandas as pd
from pathlib import Path


def load_cdi_parquet(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df ["data"]= pd.to_datetime(df["data"])

    return df 

def filter_cdi_by_date(
        df: pd.DataFrame, 
        start_date, 
        end_date,
) -> pd.DataFrame:
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[
        (df["data"] >= start_date) &
        (df["data"] <= end_date) 
    ].copy()

    return filtered_df

