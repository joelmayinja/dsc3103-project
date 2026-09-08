#%%
import pandas as pd

from src.validate.rules import rule_positive_price, rule_duplicate_ids,rule_duplicate_rows,rule_valid_date,rule_missing_market,rule_known_commodity
# %%
df = pd.read_csv("data/raw/prices.csv")

#call the rules
negative_prices = rule_positive_price(df)

duplicate_ids = rule_duplicate_ids(df)
duplicate_rows = rule_duplicate_rows(df)
invalid_dates = rule_valid_date(df)
missing_market = rule_missing_market(df)
unknown_commodity = rule_known_commodity(df, ["maize", "beans"])



print("---- Negative Prices ----")
print(negative_prices)

print("---- Duplicate IDs ----")
print(duplicate_ids)

print("---- Duplicate Rows ----")
print(duplicate_rows)

print("---- Invalid Dates ----")
print(invalid_dates)

print("---- Missing Markets ----")
print(missing_market)

print("---- Unknown Commodities ----")
print(unknown_commodity)