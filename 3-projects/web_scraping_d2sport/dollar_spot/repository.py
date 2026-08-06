from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .config import DEFAULT_PARQUET_PATH
from .domain import SpotRates


class ParquetSpotRepository:
    def __init__(self, path: Path = DEFAULT_PARQUET_PATH):
        self.path = Path(path)

    def save(self, rates: SpotRates) -> Path:
        return self.save_many([rates])

    def existing_dates(self) -> set:
        if not self.path.exists():
            return set()
        history = pd.read_parquet(self.path, columns=["reference_date"])
        return set(pd.to_datetime(history["reference_date"]).dt.date)

    def save_many(self, rates: list[SpotRates]) -> Path:
        if not rates:
            return self.path

        collected_at = datetime.now(timezone.utc)
        new_rows = pd.DataFrame([
            {
                **item.as_dict(),
                "collected_at_utc": collected_at,
            }
            for item in rates
        ])

        if self.path.exists():
            history = pd.concat(
                [pd.read_parquet(self.path), new_rows], ignore_index=True
            )
        else:
            history = new_rows

        history = (
            history.drop_duplicates(subset=["reference_date"], keep="last")
            .sort_values("reference_date")
            .reset_index(drop=True)
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        history.to_parquet(self.path, index=False, engine="pyarrow")
        return self.path
