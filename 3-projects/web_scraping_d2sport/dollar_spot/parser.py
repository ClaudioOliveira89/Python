import json
import re
import unicodedata
from datetime import datetime
from decimal import Decimal

from .domain import SpotRates


def normalize_label(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(
        char for char in normalized if not unicodedata.combining(char)
    ).lower()


def parse_decimal(value: str) -> Decimal:
    return Decimal(value.replace(".", "").replace(",", "."))


def extract_spot_rates(payload: str) -> SpotRates:
    parsed = json.loads(payload)
    if isinstance(parsed, str):
        parsed = json.loads(parsed)
    if not isinstance(parsed, list):
        raise ValueError("A resposta da B3 não contém uma lista de indicadores.")

    rates = {}
    reference_dates = set()

    for item in parsed:
        description = normalize_label(str(item.get("description", "")))
        day = None
        if re.search(r"dolar\s+spot\s+bmf\s+para\s+1\s+dia", description):
            day = "1"
        else:
            match = re.search(
                r"dolar\s+(?:bmf\s+spot|spot\s+bmf)\s*(?:-|para)?\s*([12])\s+dias?",
                description,
            )
            if match:
                day = match.group(1)

        if day is None:
            continue

        value = item.get("value") or item.get("rate")
        last_update = item.get("lastUpdate")
        if not value or not last_update:
            continue

        rates[f"spot_d{day}"] = parse_decimal(str(value))
        reference_dates.add(datetime.strptime(last_update, "%d/%m/%Y").date())

    missing = [name for name in ("spot_d1", "spot_d2") if name not in rates]
    if missing:
        raise ValueError(
            f"Indicadores não encontrados na resposta da B3: {', '.join(missing)}"
        )
    if len(reference_dates) != 1:
        raise ValueError("As cotações D+1 e D+2 possuem datas diferentes.")

    return SpotRates(
        reference_date=reference_dates.pop(),
        spot_d1=rates["spot_d1"],
        spot_d2=rates["spot_d2"],
    )
