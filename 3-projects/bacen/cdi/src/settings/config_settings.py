from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

BACEN_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"

CDI_SERIE = 12
BUSINESS_DAYS_YEAR = 252
REQUEST_TIMEOUT = 30
CHUNK_YEARS = 5