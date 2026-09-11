import pandas as pd

from src.validate.rules import (
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_known_commodity,
    rule_missing_market,
    rule_positive_price,
    rule_valid_date,
)


from src.ingest.source_a import ingest_source_a #We are in check .py and we are importing the ingest_source_a function from source_a.py to use it here. This is done to avoid hard coding the path to the source data in multiple places, making the code more maintainable and flexible.

df = pd.read_csv("data/raw/prices.csv")

rules = [
    ("Negative Prices", rule_positive_price),
    ("Duplicate IDs", rule_duplicate_ids),
    ("Duplicate Rows", rule_duplicate_rows),
    ("Invalid Dates", rule_valid_date),
    ("Missing Markets", rule_missing_market),
    ("Unknown Commodities", lambda frame: rule_known_commodity(frame, ["maize", "beans"])),
]

for name, rule_fn in rules:
    failures = rule_fn(df)
    print(f"---- {name} ----")
    print(f"Count: {len(failures)}")
    print(failures.head())
    print()


source_a = ingest_source_a()
print("---- Source A shape ----")
print(source_a.shape)