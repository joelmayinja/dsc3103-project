
def rule_positive_price(df):
    neg_prices = df[df["price"] < 0].copy()
    neg_prices["Reason"] = "negative prices"
    return neg_prices

def rule_duplicate_ids(df):
    dup_id = df["Id"].duplicated(keep="first")
    dup_id_row = df[dup_id].copy()
    dup_id_row["Reason"] = "duplicate Ids"
    return dup_id_row

def rule_duplicate_rows(df):
    dup_rows = df.duplicated(keep="first")
    dup_rows_noticed = df[dup_rows].copy()
    dup_rows_noticed["Reason"] = "duplicate rows"
    return dup_rows_noticed

def rule_valid_date_format(df):
    invalid_dates = df[~df["date"].str.match(r"\d{4}-\d{2}-\d{2}")].copy()
    invalid_dates["Reason"] = "invalid date format"
    return invalid_dates

def rule_missing_markets(df):
    missing_markets = df[df["markets"].isnull()].copy()
    missing_markets["Reason"] = "missing markets"
    return missing_markets

def rule_known_commodities(df, known_commodities):
    unknown_commodities = df[~df["Comodities"].isin(known_commodities)].copy()
    unknown_commodities["Reason"] = "unknown commodities"
    return unknown_commodities