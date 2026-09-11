import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.validate import rules

raw_path = "data/raw/prices.csv"


def inferred_schema(df):
    return df.dtypes.astype(str).to_dict()


def row_count(df):
    return len(df)


def count_missing_values(df):
    return df.isna().sum().to_dict()


def duplicate_counts(df):
    return {
        "exact_row_duplicates": int(df.duplicated().sum()),
        "duplicate_record_ids": int(rules.rule_duplicate_ids(df).shape[0]),
    }


def invalid_value_summary(df):
    return {
        "negative_or_zero_prices": int(rules.rule_positive_price(df).shape[0]),
        "invalid_dates": int(rules.rule_valid_date(df).shape[0]),
        "missing_markets": int(rules.rule_missing_market(df).shape[0]),
        "unknown_commodities": int(rules.rule_known_commodity(df, ["maize", "beans"]).shape[0]),
    }


def numeric_summary(df):
    return df.select_dtypes(include="number").describe().transpose().to_dict()


def price_histogram(df, output_path="docs/price_histogram.png"):
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"].dropna(), bins=12, edgecolor="black")
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def run_profiler(path=raw_path):
    df = pd.read_csv(path)
    report = {
        "schema": inferred_schema(df),
        "row_count": row_count(df),
        "missing_values": count_missing_values(df),
        "duplicates": duplicate_counts(df),
        "invalid_values": invalid_value_summary(df),
        "numeric_summary": numeric_summary(df),
        "histogram_path": price_histogram(df),
    }

    print("\n---- Inferred Schema ----")
    print(report["schema"])
    print("\n---- Row Count ----")
    print(report["row_count"])
    print("\n---- Missing Values ----")
    print(report["missing_values"])
    print("\n---- Duplicate Counts ----")
    print(report["duplicates"])
    print("\n---- Invalid Values ----")
    print(report["invalid_values"])
    print("\n---- Numeric Summary ----")
    for key, value in report["numeric_summary"].items():
        print(key, value)
    print(f"\nHistogram saved to: {report['histogram_path']}")
    return report


if __name__ == "__main__":
    run_profiler("data/raw/prices.csv")

   