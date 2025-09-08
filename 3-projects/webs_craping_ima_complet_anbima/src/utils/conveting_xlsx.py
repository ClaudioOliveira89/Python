import pandas as pd
from pathlib import Path

def convert_xls_to_xlsx(file_xls_path: str) -> str:

    xls_path = Path(file_xls_path)
    if not xls_path.exists():
        raise FileNotFoundError(f"File not found: {xls_path}")


    df = pd.read_excel(xls_path)


    xlsx_path = xls_path.with_suffix(".xlsx")


    df.to_excel(xlsx_path, index=False)

    print(f"[OK] File converted to .xlsx: {xlsx_path}")
    print(f"[OK] Arquivo convertido para .xlsx: {xlsx_path}")
    return str(xlsx_path)
