import re
import unicodedata
from datetime import date
from decimal import Decimal

from .domain import SpotRates
def _normalize_pdf_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text)


def _parse_bdi_decimal(value: str) -> Decimal:
    """Converte valores dos PDFs, que alternam entre ponto e vírgula decimal."""
    if "," in value and "." in value:
        decimal_separator = "," if value.rfind(",") > value.rfind(".") else "."
        thousands_separator = "." if decimal_separator == "," else ","
        value = value.replace(thousands_separator, "")
        value = value.replace(decimal_separator, ".")
    elif "," in value:
        value = value.replace(",", ".")
    return Decimal(value)


def _find_rate(text: str, symbol: str) -> Decimal:
    patterns = (
        # Quadro-resumo: DOL | RTDOLD1 | descrição | 5,1234
        rf"\bDOL\s+{symbol}\b.{{0,180}}?(\d{{1,2}}[.,]\d{{4,7}})\b",
        # Tabela detalhada: símbolo | descrição | valor
        rf"\b{symbol}\b.{{0,220}}?(\d{{1,2}}[.,]\d{{4,7}})\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _parse_bdi_decimal(match.group(1))
    raise ValueError(f"Indicador {symbol} não encontrado no boletim.")


def extract_spot_rates_from_bdi_text(text: str, reference_date: date) -> SpotRates:
    normalized = _normalize_pdf_text(text)
    return SpotRates(
        reference_date=reference_date,
        spot_d1=_find_rate(normalized, "RTDOLD1"),
        spot_d2=_find_rate(normalized, "RTDOLD2"),
    )
