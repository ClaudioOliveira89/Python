#!/usr/bin/env python3
"""Baixa a planilha fixa de Mercado Secundário publicada pela ANBIMA."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URL_ARQUIVO = "https://www.anbima.com.br/informacoes/merc-sec/arqs/m26ago04.xls"
PAGINA_ORIGEM = "https://www.anbima.com.br/pt_br/informar/taxas-de-titulos-publicos.htm"


def baixar(destino: Path) -> Path:
    requisicao = Request(
        URL_ARQUIVO,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            ),
            "Accept": "application/vnd.ms-excel,application/octet-stream,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Referer": PAGINA_ORIGEM,
        },
    )

    try:
        with urlopen(requisicao, timeout=60) as resposta:
            conteudo = resposta.read()
    except HTTPError as erro:
        raise RuntimeError(f"o download direto retornou HTTP {erro.code}: {URL_ARQUIVO}") from erro
    except URLError as erro:
        raise RuntimeError(f"não foi possível acessar a ANBIMA: {erro.reason}") from erro

    # O arquivo é um .xls clássico (OLE). Também aceitamos conteúdo OOXML/ZIP
    # caso a ANBIMA altere o formato sem alterar a extensão do link.
    eh_excel = conteudo.startswith(bytes.fromhex("D0CF11E0A1B11AE1")) or conteudo.startswith(b"PK\x03\x04")
    if not eh_excel:
        inicio = conteudo[:200].decode("latin-1", errors="replace").replace("\n", " ")
        raise RuntimeError(f"a resposta não é uma planilha Excel. Início da resposta: {inicio!r}")

    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / "m26ago04.xls"
    caminho.write_bytes(conteudo)
    return caminho


def main() -> int:
    parser = argparse.ArgumentParser(description="Baixa m26ago04.xls diretamente da ANBIMA.")
    parser.add_argument(
        "--destino",
        type=Path,
        default=Path("downloads_anbima"),
        help="pasta de saída (padrão: downloads_anbima)",
    )
    args = parser.parse_args()

    try:
        caminho = baixar(args.destino)
        print(f"Baixado: {caminho.resolve()}")
        return 0
    except RuntimeError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
