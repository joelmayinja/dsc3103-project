#%%
import pandas as pd

from scr.validate.rules import rule_positive_price, rule_duplicate_ids,rule_duplicate_rows,rule_valid_date_format,rule_missing_markets,rule_known_commodities
# %%
df = pd.read_csv("data/raw/prices.csv")

#call the rules
negative_prices = rule_positive_price(df)

duplicate_ids = rule_duplicate_ids(df)
duplicate_rows = rule_duplicate_rows(df)
invalid_dates = rule_valid_date_format(df)
missing_markets = rule_missing_markets(df)
unknown_commodities = rule_known_commodities(df, ["Commodity1", "Commodity2"])  # Replace with actual known commodities



print("---- Negative Prices ----")
print(negative_prices)

print("---- Duplicate IDs ----")
print(duplicate_ids)

print("---- Duplicate Rows ----")
print(duplicate_rows)

print("---- Invalid Dates ----")
print(invalid_dates)

print("---- Missing Markets ----")
print(missing_markets)

print("---- Unknown Commodities ----")
print(unknown_commodities)