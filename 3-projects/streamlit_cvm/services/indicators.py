
def calculate_return(df):

    initial = df["Cotação Atual"].iloc[0]
    final = df["Cotação Anterior"].iloc[-1]

    return ((final - initial)/ initial) * 100
