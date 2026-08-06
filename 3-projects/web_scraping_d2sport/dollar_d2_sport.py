"""Ponto de entrada legado para a coleta do Dólar Spot da B3."""

from pathlib import Path

from dollar_spot.cli import main
from dollar_spot.config import DEFAULT_PARQUET_PATH
from dollar_spot.parser import extract_spot_rates as _extract_spot_rates
from dollar_spot.parser import normalize_label, parse_decimal
from dollar_spot.repository import ParquetSpotRepository
from dollar_spot.service import DollarSpotService


def extract_spot_rates(payload: str) -> dict:
    return _extract_spot_rates(payload).as_dict()


def extract_spot_d2(payload: str) -> dict:
    result = extract_spot_rates(payload)
    return {
        "spot_d2": result["spot_d2"],
        "reference_date": result["reference_date"],
    }


def save_history(result: dict, parquet_path: Path = DEFAULT_PARQUET_PATH) -> Path:
    rates = _extract_spot_rates_from_dict(result)
    return ParquetSpotRepository(parquet_path).save(rates)


def _extract_spot_rates_from_dict(result: dict):
    from dollar_spot.domain import SpotRates

    return SpotRates(
        reference_date=result["reference_date"],
        spot_d1=result["spot_d1"],
        spot_d2=result["spot_d2"],
    )


def collect() -> dict:
    result = DollarSpotService().collect_and_save()
    return {
        **result.rates.as_dict(),
        "raw_content": result.raw_content,
        "source_url": result.source_url,
        "parquet_path": result.parquet_path,
    }


if __name__ == "__main__":
    main()
