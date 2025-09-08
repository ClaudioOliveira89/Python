from src.pipeline.ptax_pipeline import run_ptax_pipeline

if __name__ == "__main__":
    START_DATE = "07-07-2025"
    END_DATE = "hoje"

    run_ptax_pipeline(START_DATE, END_DATE)
