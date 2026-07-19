
def save_parquet(df, path):
    df.to_parquet(path, index=False, engine="pyarrow")

def save_csv(df, path):
    df.to_csv(path, index=False, sep=";", decimal=",")