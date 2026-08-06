from datetime import date
from decimal import Decimal

import pandas as pd

import dollar_d2_sport as scraper
from dollar_spot.backfill import business_days
from dollar_spot.bdi_client import B3DailyBulletinClient, BulletinNotFoundError
from dollar_spot.bdi_parser import extract_spot_rates_from_bdi_text
from dollar_spot.checkpoint import BackfillCheckpoint
from dollar_spot.domain import SpotRates


PAYLOAD = (
    '[{"description":"DOLAR SPOT BMF PARA 1 DIA","value":"5,0721",'
    '"lastUpdate":"31/07/2026"},'
    '{"description":"DÓLAR BMF SPOT - 2 DIAS","value":"5,0754",'
    '"lastUpdate":"31/07/2026"}]'
)


def test_extract_spot_rates_from_proxy_json():
    result = scraper.extract_spot_rates(PAYLOAD)

    assert result["spot_d1"] == Decimal("5.0721")
    assert result["spot_d2"] == Decimal("5.0754")
    assert result["reference_date"] == date(2026, 7, 31)


def test_extract_accepts_alternative_d1_label():
    payload = PAYLOAD.replace(
        "DOLAR SPOT BMF PARA 1 DIA", "DÓLAR BMF SPOT - 1 DIA"
    )

    result = scraper.extract_spot_rates(payload)

    assert result["spot_d1"] == Decimal("5.0721")


def test_save_history_replaces_same_reference_date(tmp_path):
    path = tmp_path / "history.parquet"
    first = scraper.extract_spot_rates(PAYLOAD)
    scraper.save_history(first, path)

    updated = {**first, "spot_d2": Decimal("5.0800")}
    scraper.save_history(updated, path)

    history = pd.read_parquet(path)
    assert len(history) == 1
    assert history.loc[0, "spot_d1"] == Decimal("5.0721")
    assert history.loc[0, "spot_d2"] == Decimal("5.0800")
    assert str(history["collected_at_utc"].dt.tz) == "UTC"


def test_extract_spot_rates_from_bdi_text():
    text = """
    Ativo Instrumento financeiro Descrição Preço
    DOL RTDOLD2 Indicadores gerais 5,5194
    DOL RTDOLD1 Indicador Econômico 5,5169
    """

    result = extract_spot_rates_from_bdi_text(text, date(2025, 12, 17))

    assert result.spot_d1 == Decimal("5.5169")
    assert result.spot_d2 == Decimal("5.5194")


def test_extract_spot_rates_from_bdi_with_dot_decimal():
    text = """
    DOL Futuro de Reais por Dólares Moedas RTDOLD1
    DÓLAR B3 SPOT - 1 DIA 5.5448000
    DOL Futuro de Reais por Dólares Moedas RTDOLD2
    DÓLAR B3 SPOT - 2 DIAS 5.5459000
    """

    result = extract_spot_rates_from_bdi_text(text, date(2025, 7, 11))

    assert result.spot_d1 == Decimal("5.5448000")
    assert result.spot_d2 == Decimal("5.5459000")


def test_business_days_ignores_weekend():
    result = list(business_days(date(2026, 7, 31), date(2026, 8, 3)))

    assert result == [date(2026, 7, 31), date(2026, 8, 3)]


def test_business_days_ignores_b3_holidays():
    result = list(business_days(date(2025, 3, 3), date(2025, 3, 5)))

    assert result == [date(2025, 3, 5)]


def test_bdi_client_treats_server_error_as_missing_bulletin():
    class Response:
        status_code = 500

    class Session:
        def get(self, *args, **kwargs):
            return Response()

    client = B3DailyBulletinClient(session=Session())

    try:
        client.fetch(date(2025, 1, 1))
    except BulletinNotFoundError:
        pass
    else:
        raise AssertionError("Era esperado BulletinNotFoundError")


def test_bdi_client_includes_old_bdi_00_filename():
    urls = B3DailyBulletinClient.candidate_urls(date(2023, 7, 21))

    assert any("BDI_00_20230721_en-Us.pdf" in url for url in urls)


def test_checkpoint_recovers_last_collected_rate(tmp_path):
    checkpoint = BackfillCheckpoint(tmp_path / "checkpoint.jsonl")
    expected = SpotRates(
        reference_date=date(2025, 12, 17),
        spot_d1=Decimal("5.5169"),
        spot_d2=Decimal("5.5194"),
    )

    checkpoint.append(expected)

    assert checkpoint.load() == [expected]
