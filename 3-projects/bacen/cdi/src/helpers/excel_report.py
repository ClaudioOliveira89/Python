import pandas as pd

from src.settings.config_settings import REPORTS_DIR
from src.utils.logger import setup_logging


logger = setup_logging(__name__)


def save_cdi_report(df: pd.DataFrame, filename: str = "cdi_bacen.xlsx") -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = REPORTS_DIR / filename

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="CDI", index=False)

        worksheet = writer.sheets["CDI"]

        for column_cells in worksheet.columns:
            max_length = 0
            column_letter = column_cells[0].column_letter
            column_name = column_cells[0].value

            for cell in column_cells:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))

            worksheet.column_dimensions[column_letter].width = max_length + 2

            if column_name == "data":
                for cell in column_cells[1:]:
                    cell.number_format = "dd/mm/yyyy"

    logger.info("Relatório salvo em: %s", output_path)

    return str(output_path)