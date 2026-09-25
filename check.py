from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
from src.validate.rules import (
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_known_commodity,
    rule_missing_market,
    rule_negative_rain,
    rule_positive_price,
    rule_valid_date,
)


def main():
    source_a = ingest_source_a()
    source_b = ingest_source_b()

    validation_rules = [
        ("Negative Prices", rule_positive_price),
        ("Duplicate IDs", rule_duplicate_ids),
        ("Duplicate Rows", rule_duplicate_rows),
        ("Invalid Dates", rule_valid_date),
        ("Missing Markets", rule_missing_market),
        (
            "Unknown Commodities",
            lambda frame: rule_known_commodity(frame, ["maize", "beans"]),
        ),
    ]

    for name, rule in validation_rules:
        failures = rule(source_a)
        print(f"---- {name} ----")
        print(f"Count: {len(failures)}")
        print(failures.head())

    print("---- Source A shape ----")
    print(source_a.shape)
    print("---- Source B shape ----")
    print(source_b.shape)

    clean_prices, cleaning_log = clean_data()
    print("---- Cleaned prices ----")
    print(f"Rows: {len(clean_prices)}")
    for message in cleaning_log:
        print(message)

    negative_rainfall = rule_negative_rain(source_b)
    print("---- Negative Rainfall ----")
    print(f"Count: {len(negative_rainfall)}")

    merged_data = merge_data(clean_prices, source_b)
    print("---- Merged Data ----")
    print(f"Shape: {merged_data.shape}")
    print(merged_data.head())
    return merged_data


if __name__ == "__main__":
    main()
