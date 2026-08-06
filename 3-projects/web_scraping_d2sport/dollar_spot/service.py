from dataclasses import dataclass
from pathlib import Path

from .b3_client import B3FinancialIndicatorsClient
from .domain import SpotRates
from .parser import extract_spot_rates
from .repository import ParquetSpotRepository


@dataclass(frozen=True)
class CollectionResult:
    rates: SpotRates
    parquet_path: Path
    raw_content: bytes
    source_url: str


class DollarSpotService:
    def __init__(self, client=None, repository=None):
        self.client = client or B3FinancialIndicatorsClient()
        self.repository = repository or ParquetSpotRepository()

    def collect_and_save(self) -> CollectionResult:
        payload, raw_content, source_url = self.client.fetch()
        rates = extract_spot_rates(payload)
        parquet_path = self.repository.save(rates)
        return CollectionResult(
            rates=rates,
            parquet_path=parquet_path,
            raw_content=raw_content,
            source_url=source_url,
        )
