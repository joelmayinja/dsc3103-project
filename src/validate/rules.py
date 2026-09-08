import pandas as pd
from datetime import datetime

def rule_positive_price(df):
    neg_prices = df[df["price"] < 0].copy()
    neg_prices["Reason"]="Negative Price"
    return neg_prices

def rule_duplicate_ids(df):
    # Create a mask for rows where the ID has appeared before
    # keep='first' (default) marks the 2nd, 3rd, etc. occurrences as True
    dup_mask = df["Id"].duplicated(keep="first")
    
    # Filter the dataframe to only keep those duplicate rows
    dup_rows = df[dup_mask].copy()
    
    # Add the Reason column to match your framework's pattern
    dup_rows["Reason"] = "Duplicate ID"
    
    return dup_rows

def rule_duplicate_rows(df):
    # Checks for entirely identical rows across all columns
    # keep='first' flags the subsequent copies as duplicates
    dup_row_mask = df.duplicated(keep="first")
    
    # Filter the dataframe to isolate the duplicate rows
    dup_rows = df[dup_row_mask].copy()
    
    # Add the validation framework reason
    dup_rows["Reason"] = "Duplicate Row"
    
    return dup_rows

def rule_valid_date(df):
    # convert date column to datetime objects; invalid formates turn to Not a Time(NaT)
    converted_date = pd.to_datetime(df["date"], errors="coerce")

    # find columns where conversion failed or time is in the future
    invalid_mask = converted_date.isnull() | (converted_date > datetime.now())

    # extract invalid rows, add reason
    invalid_rows = df[invalid_mask].copy()
    invalid_rows["Reason"] = "Invalid or Future date"

    return invalid_rows

def rule_missing_market(df):
    # find rows where market name is null
    missing_mark = (df["markets"].isnull()) | (df["markets"] == "")

    # extract rows, columns
    missing_rows = df[missing_mark].copy()
    missing_rows["Reason"] = "Missing market"

    return missing_rows

def rule_known_commodity(df, known_commodity):
    # find rows where commodity is not in the known list
    known_values = {commodity.lower() for commodity in known_commodity}
    unknown_mask = ~df["Comodities"].fillna("").str.lower().isin(known_values)

    # extract rows, add reason
    unknown_row = df[unknown_mask].copy()
    unknown_row["Reason"] = "Unknown Commodity"

    return unknown_row