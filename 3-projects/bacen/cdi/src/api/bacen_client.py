import requests
import pandas as pd 
from src.settings.config_settings import BACEN_BASE_URL, REQUEST_TIMEOUT
from src.utils.date_utils import format_date_br
from src.utils.logger import setup_logging

logger = setup_logging(__name__)

class BacenClient:
    def __init__(self):
        self.base_url = BACEN_BASE_URL

    def get_sgs_series(
        self,
        serie: int,
        start_date,
        end_date
    ) -> pd.DataFrame:
        
        url = self.base_url.format(serie=serie)

        params = {
            "formato": "json",
            "dataInicial": format_date_br(start_date),
            "dataFinal": format_date_br(end_date),
        }

        logger.info(
        "Consultando Bacen SGS série %s de %s até %s",
        serie,
        params["dataInicial"],
        params["dataFinal"],
        )

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            logger.warning(
                "Nenhum dado retornado para série %s entre %s e %s",
                serie,
                params["dataInicial"],
                params["dataFinal"],
            )
            return pd.DataFrame(columns=["data", "valor"])

        df = pd.DataFrame(data)

        return df