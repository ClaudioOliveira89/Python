from .service import DollarSpotService


def main() -> None:
    result = DollarSpotService().collect_and_save()
    rates = result.rates
    print(
        rates.reference_date,
        f"D+1: {rates.spot_d1}",
        f"D+2: {rates.spot_d2}",
    )
    print(f"Histórico salvo em: {result.parquet_path}")


if __name__ == "__main__":
    main()
