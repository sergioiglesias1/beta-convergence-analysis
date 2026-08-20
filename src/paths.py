from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "results" / "figures"
TABLES_DIR = ROOT / "results" / "tables"

CLEAN_DATA = PROCESSED_DIR / "clean_data.csv"
SIGMA_DATA = PROCESSED_DIR / "sigma_convergence.csv"
