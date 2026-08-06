from pathlib import Path


B3_PROXY_URL = (
    "https://sistemaswebb3-derivativos.b3.com.br/"
    "financialIndicatorsProxy/FinancialIndicators/"
    "GetFinancialIndicators/{encoded_payload}"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PARQUET_PATH = PROJECT_ROOT / "data" / "dollar_spot_history.parquet"
DEFAULT_CHECKPOINT_PATH = PROJECT_ROOT / "data" / "backfill_checkpoint.jsonl"
DEFAULT_LOG_PATH = PROJECT_ROOT / "logs" / "backfill.log"
