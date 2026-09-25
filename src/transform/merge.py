
import pandas as pd


def merge_data(clean_df, rainfall_df):
    return clean_df.merge(rainfall_df, on=["date", "market"], how="left", validate="many_to_one")