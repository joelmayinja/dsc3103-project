import pandas as pd
from pathlib import Path

from src.common.config import SOURCE_A_RAW_PATH


def ingest_source_a(path: str | Path = SOURCE_A_RAW_PATH) -> pd.DataFrame:
    source_path = Path(path)
    if not source_path.is_file():
        raise FileNotFoundError(f"Source A file was not found: {source_path}")
    return pd.read_csv(source_path)