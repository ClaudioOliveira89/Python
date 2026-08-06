"""Coleta e armazenamento das cotações de Dólar Spot da B3."""

from .domain import SpotRates
from .service import DollarSpotService

__all__ = ["DollarSpotService", "SpotRates"]
