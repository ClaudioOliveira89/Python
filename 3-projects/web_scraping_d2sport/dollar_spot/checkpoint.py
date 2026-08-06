import json
import os
from datetime import date
from decimal import Decimal
from pathlib import Path

from .config import DEFAULT_CHECKPOINT_PATH
from .domain import SpotRates


class BackfillCheckpoint:
    """Diário durável das cotações coletadas durante o backfill."""

    def __init__(self, path: Path = DEFAULT_CHECKPOINT_PATH):
        self.path = Path(path)

    def append(self, rates: SpotRates) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "reference_date": rates.reference_date.isoformat(),
            "spot_d1": str(rates.spot_d1),
            "spot_d2": str(rates.spot_d2),
        }
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            file.flush()
            os.fsync(file.fileno())

    def load(self) -> list[SpotRates]:
        if not self.path.exists():
            return []

        by_date = {}
        with self.path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    rates = SpotRates(
                        reference_date=date.fromisoformat(record["reference_date"]),
                        spot_d1=Decimal(record["spot_d1"]),
                        spot_d2=Decimal(record["spot_d2"]),
                    )
                except (KeyError, ValueError, json.JSONDecodeError):
                    # Uma última linha parcial pode existir se o processo foi
                    # encerrado exatamente durante a escrita.
                    continue
                by_date[rates.reference_date] = rates
        return list(by_date.values())
