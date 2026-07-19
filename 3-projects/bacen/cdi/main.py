import argparse
from src.pipeline.cdi_pipeline import CDIPipeline
from src.api.bacen_client import BacenClient
from src.helpers.excel_report import save_cdi_report
from src.utils.date_utils import parse_date_br, today
from src.utils.logger import setup_logging
from src.settings.config_settings import RAW_DIR, PROCESSED_DIR


logger = setup_logging(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline para extrair CDI da API SGS/Bacen"
    )
    parser.add_argument(
    "--start", 
    required=True, 
    help="Data inicial no formanto DD/MM/YYYY. Exemplo: 01/01/2010", 
    ) 

    args = parser.parse_args()

    start_date = parse_date_br(args.start)
    end_date = today()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pipeline = CDIPipeline()

    df_cdi = pipeline.run(
        start_date=start_date, 
        end_date=end_date, 
    )

    if df_cdi.empty:
        logger.warning("Nenum dado de CDI encontrado.")
        return
    
    csv_path = PROCESSED_DIR / "cdi_bacen.csv"
    parquet_path = PROCESSED_DIR / "cdi_bacen.parquet"

    df_cdi.to_csv(
        csv_path,
        index=False, 
        sep=";", 
        decimal=";" 
    )

    df_cdi.to_parquet(
        parquet_path, 
        index=False,
        engine="pyarrow"
    )

    report_path = save_cdi_report(df_cdi)

    logger.info("CSV salvo em: %s", csv_path)
    logger.info("Parquet salvo em: %s", parquet_path)
    logger.info("Relatório Excel salvo em: %s", report_path)

    print(df_cdi.tail())
    print(f"\nCSV salvo em: {csv_path}")
    print(f"Parquet salvo em: {parquet_path}")
    print(f"Excel salvo em: {report_path}")

if __name__ == "__main__":
    main()