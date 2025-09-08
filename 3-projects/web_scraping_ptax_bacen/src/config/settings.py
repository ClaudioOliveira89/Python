from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOWNLOAD_DIR = BASE_DIR /"downloads"
REPORT_DIR = BASE_DIR /"report"



DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PTAX_FILE = DOWNLOAD_DIR / "ptax.xlsx"

PTAX_ENDPOINT = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{date}'&$format=json"
)

DATE_FORMAT_INPUT = "%d-%m-%Y"
DATE_FORMAT_OUTPUT = "%d/%m/%Y %H:%M:%S"

