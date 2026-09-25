import pandas as pd


def _canonicalize_columns(df):
    renamed = df.copy()
    rename_map = {
        "Id": "record_id",
        "record_id": "record_id",
        "date": "date",
        "market": "market",
        "markets": "market",
        "commodity": "commodity",
        "commodities": "commodity",
        "comodities": "commodity",
        "price": "price",
    }
    lower_map = {str(column).strip().lower(): str(column) for column in renamed.columns}
    new_columns = []
    for column in renamed.columns:
        lower_name = str(column).strip().lower()
        canonical = rename_map.get(column, rename_map.get(lower_name))
        if canonical:
            new_columns.append(canonical)
        else:
            new_columns.append(lower_name)
    renamed.columns = new_columns
    return renamed


def rule_positive_price(df):
    df_clean = _canonicalize_columns(df)
    invalid_rows = df_clean[df_clean["price"] <= 0].copy()
    invalid_rows["Reason"] = "Negative or non-positive price"
    return invalid_rows


def rule_duplicate_ids(df):
    df_clean = _canonicalize_columns(df)
    duplicate_mask = df_clean["record_id"].duplicated(keep="first")
    duplicate_rows = df_clean[duplicate_mask].copy()
    duplicate_rows["Reason"] = "Duplicate ID"
    return duplicate_rows


def rule_duplicate_rows(df):
    df_clean = _canonicalize_columns(df)
    duplicate_mask = df_clean.duplicated(keep="first")
    duplicate_rows = df_clean[duplicate_mask].copy()
    duplicate_rows["Reason"] = "Duplicate Row"
    return duplicate_rows


def rule_valid_date(df):
    df_clean = _canonicalize_columns(df)
    converted_date = pd.to_datetime(df_clean["date"], errors="coerce")
    invalid_mask = converted_date.isnull() | (converted_date > pd.Timestamp.now())
    invalid_rows = df_clean[invalid_mask].copy()
    invalid_rows["Reason"] = "Invalid or future date"
    return invalid_rows


def rule_missing_market(df):
    df_clean = _canonicalize_columns(df)
    missing_mask = df_clean["market"].isna() | df_clean["market"].astype(str).str.strip().eq("")
    missing_rows = df_clean[missing_mask].copy()
    missing_rows["Reason"] = "Missing market"
    return missing_rows


def rule_known_commodity(df, known_commodities=None):
    df_clean = _canonicalize_columns(df)
    if known_commodities is None:
        known_commodities = ["Maize", "Beans"]
    known_values = {str(item).strip().lower() for item in known_commodities}
    commodity_values = df_clean["commodity"].fillna("").astype(str).str.strip().str.lower()
    unknown_mask = ~commodity_values.isin(known_values)
    unknown_rows = df_clean[unknown_mask].copy()
    unknown_rows["Reason"] = "Unknown commodity"
    return unknown_rows


def rule_negative_rain(df):
   neg_rain = df[df['rainfall_mm'] < 0].copy()
   neg_rain['Reason'] = 'Negative rainfall'
   return neg_rain