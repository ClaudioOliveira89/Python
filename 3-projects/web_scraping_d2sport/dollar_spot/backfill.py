import argparse
import logging
import time
from datetime import date, timedelta
from logging.handlers import RotatingFileHandler

import requests
from pypdf.errors import PdfReadError

from .bdi_client import B3DailyBulletinClient, BulletinNotFoundError
from .checkpoint import BackfillCheckpoint
from .config import DEFAULT_LOG_PATH
from .market_calendar import is_b3_trading_day
from .repository import ParquetSpotRepository


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("dollar_spot.backfill")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)sZ | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    formatter.converter = time.gmtime
    DEFAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        DEFAULT_LOG_PATH,
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)
    return logger


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Use uma data no formato AAAA-MM-DD."
        ) from error


def business_days(start: date, end: date):
    current = start
    while current <= end:
        if is_b3_trading_day(current):
            yield current
        current += timedelta(days=1)


def run_backfill(start: date, end: date) -> tuple[int, int]:
    if start > end:
        raise ValueError("A data inicial não pode ser posterior à data final.")

    logger = configure_logging()
    client = B3DailyBulletinClient()
    repository = ParquetSpotRepository()
    checkpoint = BackfillCheckpoint()

    recovered = checkpoint.load()
    if recovered:
        repository.save_many(recovered)
        logger.info("Checkpoint recuperado: %s datas consolidadas.", len(recovered))

    existing_dates = repository.existing_dates()
    collected = []
    saved_count = 0
    unavailable = 0

    period_dates = list(business_days(start, end))
    dates = [day for day in period_dates if day not in existing_dates]
    total = len(dates)
    logger.info(
        "Iniciando período %s a %s; %s já existentes; %s pendentes.",
        start,
        end,
        len(period_dates) - total,
        total,
    )

    for position, reference_date in enumerate(dates, start=1):
        prefix = f"[{position}/{total}] {reference_date.isoformat()}"
        try:
            rates = client.fetch(reference_date)
        except BulletinNotFoundError:
            unavailable += 1
            logger.info("%s sem boletim", prefix)
            continue
        except ValueError as error:
            unavailable += 1
            logger.warning("%s sem indicadores (%s)", prefix, error)
            continue
        except (requests.RequestException, PdfReadError) as error:
            unavailable += 1
            logger.error("%s falha no download/PDF (%s)", prefix, error)
            continue

        # O checkpoint é sincronizado no disco antes de avançar para a
        # próxima data. Assim, até o último resultado pode ser recuperado.
        checkpoint.append(rates)
        collected.append(rates)
        logger.info("%s D+1=%s D+2=%s", prefix, rates.spot_d1, rates.spot_d2)

        if len(collected) >= 20:
            repository.save_many(collected)
            saved_count += len(collected)
            collected.clear()
            logger.info("Checkpoint Parquet: %s novas datas salvas.", saved_count)

    if collected:
        repository.save_many(collected)
        saved_count += len(collected)

    logger.info(
        "Concluído: %s datas incluídas; %s indisponíveis.",
        saved_count,
        unavailable,
    )
    return saved_count, unavailable


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Carrega o histórico D+1 e D+2 dos boletins da B3."
    )
    parser.add_argument("--inicio", required=True, type=parse_date)
    parser.add_argument("--fim", required=True, type=parse_date)
    args = parser.parse_args()
    run_backfill(args.inicio, args.fim)


if __name__ == "__main__":
    main()
