from openpyxl import Workbook
from pathlib import Path

def write_to_excel(data, file_path):
    file_path = Path(file_path)
    workbook = Workbook()
    sheet = workbook.active

    for row in data:
        sheet.append(row)

    workbook.save(file_path)

