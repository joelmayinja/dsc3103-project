from pathlib import Path

import pandas as pd
import requests

from src.common.config import (
    MARKET_COORDS,
    RAINFALL_END_DATE,
    RAINFALL_START_DATE,
    RAINFALL_URL,
    SOURCE_B_RAW_PATH,
)


def get_market_rainfall(
    market_name: str,
    latitude: float,
    longitude: float,
    start_date: str = RAINFALL_START_DATE,
    end_date: str = RAINFALL_END_DATE,
) -> pd.DataFrame:
    response = requests.get(
        RAINFALL_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto",
            "daily": "precipitation_sum",
        },
        timeout=10,
    )
    response.raise_for_status()
    daily = response.json()["daily"]
    return pd.DataFrame(
        {
            "date": daily["time"],
            "rainfall_mm": daily["precipitation_sum"],
            "market": market_name,
        }
    )


def get_all_markets_rainfall() -> pd.DataFrame:
    frames = [
        get_market_rainfall(market, latitude, longitude)
        for market, (latitude, longitude) in MARKET_COORDS.items()
    ]
    return pd.concat(frames, ignore_index=True)


def ingest_source_b(path: str | Path = SOURCE_B_RAW_PATH) -> pd.DataFrame:
    source_path = Path(path)
    if source_path.is_file():
        return pd.read_csv(source_path)

    source_path.parent.mkdir(parents=True, exist_ok=True)
    rainfall = get_all_markets_rainfall()
    rainfall.to_csv(source_path, index=False)
    return rainfall
