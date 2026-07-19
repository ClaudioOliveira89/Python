import pandas as pd
from src.api.bacen_client import BacenClient
from src.settings.config_settings import CDI_SERIE, BUSINESS_DAYS_YEAR, CHUNK_YEARS
from src.utils.date_utils import generate_date_chunks
from src.utils.logger import setup_logging


logger = setup_logging(__name__)


class CDIPipeline:
    def __init__(self):
        self.client = BacenClient()

    def extract(self, start_date, end_date) -> pd.DataFrame:
        chunks = generate_date_chunks(
            start_date=start_date,
            end_date=end_date,
            chunk_years=CHUNK_YEARS,
        )

        frames = []

        for chunk_start, chunk_end in chunks:
            df_chunk = self.client.get_sgs_series(
                serie=CDI_SERIE,
                start_date=chunk_start,
                end_date=chunk_end,
            )

            if not df_chunk.empty:
                frames.append(df_chunk)

        if not frames:
            return pd.DataFrame(columns=["data", "valor"])

        df = pd.concat(frames, ignore_index=True)

        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            logger.warning("DataFrame vazio recebido no transform.")
            return df

        df = df.copy()

        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

        df["taxa_cdi_ad_pct"] = (
            df["valor"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        df["taxa_cdi_ad_decimal"] = df["taxa_cdi_ad_pct"] / 100

        df["fator_diario"] = 1 + df["taxa_cdi_ad_decimal"]

        df["taxa_cdi_aa_decimal"] = (df["fator_diario"] ** BUSINESS_DAYS_YEAR) - 1

        df["taxa_cdi_aa_pct"] = df["taxa_cdi_aa_decimal"] * 100

        df = df[
            [
                "data",
                "taxa_cdi_ad_pct",
                "taxa_cdi_ad_decimal",
                "fator_diario",
                "taxa_cdi_aa_pct",
                "taxa_cdi_aa_decimal",
            ]
        ]

        df = df.sort_values("data").drop_duplicates(subset=["data"])

        return df

    def run(self, start_date, end_date) -> pd.DataFrame:
        logger.info("Iniciando pipeline CDI.")

        raw_df = self.extract(
            start_date=start_date,
            end_date=end_date,
        )

        processed_df = self.transform(raw_df)

        logger.info("Pipeline CDI finalizado. Linhas: %s", len(processed_df))

        return processed_df