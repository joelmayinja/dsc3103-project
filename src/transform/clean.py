#%%

import pandas as pd
# %%
from src.validate import rules

raw_path = "data/raw/prices.csv"

## parquet means better installation and faster reading and writing of data
data_path ="data/processed/prices_clean.parquet"


def clean_data(path=raw_path):

    df =pd.read_csv(path)

    log=[]

    duplicate_rows =rules.rule_duplicate_rows(df)
    if len(duplicate_rows)>0:
        duplicates_count = len(duplicate_rows)
        log.append("Duplicate Rows: " + str(duplicates_count))
        df = df.drop_duplicates(keep="first")
        df.drop_duplicates()

    # Remove duplicate record IDs
    duplicate_ids = rules.rule_duplicate_ids(df)
    if len(duplicate_ids) > 0:
        log.append("Removed " + str(len(duplicate_ids)) + " rows with duplicate record IDs")
        df = df.drop_duplicates(subset="record_id", keep="first")

    # Remove invalid prices
    invalid_prices = rules.rule_positive_price(df)
    if len(invalid_prices) > 0:
        log.append("Removed " + str(len(invalid_prices)) + " rows with invalid prices")
        df = df.drop(invalid_prices.index)

    # Remove invalid dates
    invalid_dates = rules.rule_valid_date(df)
    if len(invalid_dates) > 0:
        log.append("Removed " + str(len(invalid_dates)) + " rows with invalid dates")
        df = df.drop(invalid_dates.index)

    # Handle missing market values
    missing_market = rules.rule_missing_market(df)
    if len(missing_market) > 0:
        log.append("Changed " + str(len(missing_market)) + " missing market values to Unknown")
        df.loc[missing_market.index, "market"] = "Unknown"

    # Handle inconsistent commodity values
    known_commodity = rules.rule_known_commodity(df)
    if len(known_commodity) > 0:
        log.append("Found " + str(len(known_commodity)) + " inconsistent commodity values")

    # Normalize commodity names
    df["commodity"] = df["commodity"].str.strip().str.title()
    log.append("Normalized commodity names")

    # Save cleaned data
    df.to_parquet(data_path, index=False)

    return df, log



# Run cleaning
cleaned_data, cleaning_log = clean_data()

print("Cleaning completed.\n")

print("Cleaning Log:")
for item in cleaning_log:
    print("-", item)

print("\nCleaned Data:")
print(cleaned_data)

#%%
        
