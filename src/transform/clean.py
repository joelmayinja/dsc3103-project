import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from src.validate import rules

raw_path = Path("data/raw/prices.csv")
data_path = Path("data/processed/prices_clean.parquet")
report_path = Path("docs/validation_report.md")


def compute_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rename_columns(df):
    rename_map = {
        "Id": "record_id",
        "record_id": "record_id",
        "markets": "market",
        "market": "market",
        "Comodities": "commodity",
        "commodity": "commodity",
        "commodities": "commodity",
        "comodities": "commodity",
    }
    df = df.copy()
    df.columns = [rename_map.get(str(column), str(column)) for column in df.columns]
    return df


def clean_data(path=raw_path):
    before_hash = compute_hash(path)
    df = pd.read_csv(path)
    df = rename_columns(df)
    log = []

    duplicate_rows = rules.rule_duplicate_rows(df)
    if not duplicate_rows.empty:
        log.append(f"Reject: {len(duplicate_rows)} exact duplicate rows (duplicate row rule).")
        df = df.drop_duplicates(keep="first").copy()

    duplicate_ids = rules.rule_duplicate_ids(df)
    if not duplicate_ids.empty:
        log.append(f"Reject: {len(duplicate_ids)} rows with duplicate record_id values.")
        df = df.drop_duplicates(subset="record_id", keep="first").copy()

    invalid_prices = rules.rule_positive_price(df)
    if not invalid_prices.empty:
        log.append(f"Reject: {len(invalid_prices)} rows with non-positive prices.")
        df = df[df["price"] > 0].copy()

    invalid_dates = rules.rule_valid_date(df)
    if not invalid_dates.empty:
        log.append(f"Reject: {len(invalid_dates)} rows with invalid or future dates.")
        df = df[~df.index.isin(invalid_dates.index)].copy()

    missing_market = rules.rule_missing_market(df)
    if not missing_market.empty:
        log.append(f"Impute: {len(missing_market)} missing market values set to 'Unknown'.")
        df.loc[missing_market.index, "market"] = "Unknown"

    unknown_commodities = rules.rule_known_commodity(df, ["maize", "beans"])
    if not unknown_commodities.empty:
        log.append(f"Normalize: {len(unknown_commodities)} commodity spellings standardized to canonical names.")

    df["commodity"] = df["commodity"].fillna("Unknown").astype(str).str.strip().str.title()
    df["commodity"] = df["commodity"].replace({"Maiz": "Maize", "Maize ": "Maize", "Bean": "Beans"})
    df["market"] = df["market"].fillna("Unknown").astype(str).str.strip()
    df["market"] = df["market"].replace({"": "Unknown"})

    data_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(data_path, index=False)

    after_hash = compute_hash(path)
    log.append(f"Raw file preserved: {before_hash == after_hash} (sha256={before_hash}).")

    validation_rows = [
        "| Rule | Failing rows before cleaning | Action taken |",
        "| --- | ---: | --- |",
        f"| Positive price | {len(rules.rule_positive_price(pd.read_csv(path)))} | Rejected non-positive prices |",
        f"| Duplicate record_id | {len(rules.rule_duplicate_ids(pd.read_csv(path)))} | Dropped duplicate IDs, keeping first |",
        f"| Duplicate rows | {len(rules.rule_duplicate_rows(pd.read_csv(path)))} | Dropped exact duplicate rows |",
        f"| Valid date | {len(rules.rule_valid_date(pd.read_csv(path)))} | Removed invalid/future dates |",
        f"| Missing market | {len(rules.rule_missing_market(pd.read_csv(path)))} | Imputed 'Unknown' |",
        f"| Known commodity | {len(rules.rule_known_commodity(pd.read_csv(path), ['maize', 'beans']))} | Normalized commodity text |",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("# Validation report\n\n" + "\n".join(validation_rows) + "\n\n## Cleaning decisions\n\n" + "\n".join(f"- {entry}" for entry in log) + "\n", encoding="utf-8")

    return df, log


if __name__ == "__main__":
    cleaned_data, cleaning_log = clean_data(raw_path)
    print("Cleaning completed.")
    print(f"Cleaned rows: {len(cleaned_data)}")
    print("\nCleaning log:")
    for item in cleaning_log:
        print(f"- {item}")
    print(f"\nOutput: {data_path}")

