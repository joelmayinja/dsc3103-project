
import pandas as pd


def merge_data(clean_df: pd.DataFrame, rainfall_df: pd.DataFrame) -> pd.DataFrame:
    return clean_df.merge(rainfall_df, on=["date", "market"], how="left", validate="many_to_one")