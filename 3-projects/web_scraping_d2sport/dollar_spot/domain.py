from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class SpotRates:
    reference_date: date
    spot_d1: Decimal
    spot_d2: Decimal

    def as_dict(self) -> dict:
        return {
            "reference_date": self.reference_date,
            "spot_d1": self.spot_d1,
            "spot_d2": self.spot_d2,
        }
