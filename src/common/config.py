import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
SOURCE_A_RAW_PATH = Path(os.getenv("SOURCE_A_RAW_PATH", ROOT_DIR / "data/raw/prices.csv"))
SOURCE_B_RAW_PATH = Path(os.getenv("SOURCE_B_RAW_PATH", ROOT_DIR / "data/raw/rainfall.csv"))
PROCESSED_PATH = Path(os.getenv("PROCESSED_PATH", ROOT_DIR / "data/processed/prices_with_rainfall.parquet"))
QUARANTINE_PATH = Path(os.getenv("QUARANTINE_PATH", ROOT_DIR / "data/processed/quarantine.csv"))
LOG_PATH = Path(os.getenv("PIPELINE_LOG_PATH", ROOT_DIR / "docs/pipeline.log"))


MARKET_COORDS ={

    "Mukono" :(0.3539, 32.7553),
    "Bwaise" :(0.3476, 32.5610),
    "Nakasero" :(0.3233, 32.5789),
    "Kasanga" :(0.2872, 32.6078) 
}


RAINFALL_START_DATE = "2020-01-01"
RAINFALL_END_DATE = "2020-06-30"


RAINFALL_URL = os.getenv("RAINFALL_URL", "https://archive-api.open-meteo.com/v1/archive")

KNOWN_COMMODITIES = ["maize", "beans"]
MIN_PRICE = float(os.getenv("MIN_PRICE", "0"))
