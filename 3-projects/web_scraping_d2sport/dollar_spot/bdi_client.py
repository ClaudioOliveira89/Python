from datetime import date
from io import BytesIO

import requests
from pypdf import PdfReader
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .bdi_parser import extract_spot_rates_from_bdi_text
from .domain import SpotRates


BDI_BASE_URL = "https://arquivos.b3.com.br/bdi/download/bdi"


class BulletinNotFoundError(Exception):
    pass


class B3DailyBulletinClient:
    def __init__(self, timeout: int = 60, session=None):
        self.timeout = timeout
        self.session = session or self._create_session()

    @staticmethod
    def _create_session():
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=(429, 502, 503, 504),
            allowed_methods=("GET",),
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))
        return session

    @staticmethod
    def candidate_urls(reference_date: date) -> list[str]:
        iso_date = reference_date.isoformat()
        compact_date = reference_date.strftime("%Y%m%d")
        base = f"{BDI_BASE_URL}/{iso_date}"
        urls = []
        # A B3 alternou os códigos 00/02, o sufixo -0 e o idioma ao longo
        # dos anos. Todas as combinações abaixo existem no Acervo histórico.
        for bulletin_code in ("02", "00"):
            for revision in ("-0", ""):
                filename = f"BDI_{bulletin_code}{revision}_{compact_date}"
                urls.append(f"{base}/{filename}.pdf")
                urls.append(f"{base}/{filename}_en-Us.pdf")
        return urls

    def fetch(self, reference_date: date) -> SpotRates:
        last_parse_error = None
        for url in self.candidate_urls(reference_date):
            response = self.session.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=self.timeout,
            )
            # O Acervo B3 frequentemente devolve 500, em vez de 404, quando
            # não existe boletim para feriados ou para uma variante do nome.
            if response.status_code in (404, 500):
                continue
            response.raise_for_status()

            reader = PdfReader(BytesIO(response.content))
            accumulated_text = ""
            last_error = None
            for page in reader.pages:
                accumulated_text += "\n" + (page.extract_text() or "")
                try:
                    return extract_spot_rates_from_bdi_text(
                        accumulated_text, reference_date
                    )
                except ValueError as error:
                    last_error = error

            # Um nome de arquivo inexistente pode devolver um PDF genérico com
            # status 200. Nesse caso, ainda precisamos tentar o outro padrão.
            last_parse_error = last_error

        if last_parse_error is not None:
            raise ValueError(
                f"Indicadores ausentes no PDF de {reference_date}: "
                f"{last_parse_error}"
            )
        raise BulletinNotFoundError(
            f"Boletim não encontrado para {reference_date.isoformat()}"
        )
