import pandas as pd

from src.transform.merge import merge_data
from src.validate.rules import rule_negative_rain, rule_positive_price


def test_positive_price_rejects_non_positive_rows():
    frame = pd.DataFrame({"record_id": [1, 2], "price": [10, 0]})

    failures = rule_positive_price(frame)

    assert failures["record_id"].tolist() == [2]


def test_negative_rainfall_rule_rejects_negative_rows():
    frame = pd.DataFrame({"date": ["2020-01-01", "2020-01-02"], "rainfall_mm": [0.5, -1.0]})

    failures = rule_negative_rain(frame)

    assert len(failures) == 1
    assert failures.iloc[0]["Reason"] == "Negative rainfall"


def test_merge_preserves_price_rows_and_adds_rainfall():
    prices = pd.DataFrame({"record_id": [1], "date": ["2020-01-01"], "market": ["Mukono"], "price": [100]})
    rainfall = pd.DataFrame({"date": ["2020-01-01"], "market": ["Mukono"], "rainfall_mm": [2.5]})

    merged = merge_data(prices, rainfall)

    assert len(merged) == 1
    assert merged.iloc[0]["rainfall_mm"] == 2.5
