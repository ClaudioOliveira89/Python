from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def parse_date_br(date_str: str) -> date:
    return datetime.strptime(date_str, "%d/%m/%Y").date()

def format_date_br(date_value: date)-> str:
    return date_value.strftime("%d/%m/%Y")

def today() -> date:
    return date.today()

def generate_date_chunks(
    start_date,
    end_date,
    chunk_years: int = 5
):
    chunks = []

    current_start = start_date

    while current_start <= end_date:
        current_end = (
            current_start
            + relativedelta(years=chunk_years)
            - relativedelta(days=1)
        )

        if current_end > end_date:
            current_end = end_date

        chunks.append((current_start, current_end))

        current_start = current_end + relativedelta(days=1)

    return chunks