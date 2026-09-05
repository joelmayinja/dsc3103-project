#%%
import pandas as pd
# %%
from scr.validate import rules

raw_path = "data/raw/prices.csv"

## parquet means better installation and faster reading and writing of data
data_path ="data/processed/prices_clean.parquet"








def clean_data(path=raw_path):
    df =pd.read_csv(path)

    log=[]

    duplicate_rows =rules.rule_duplicate_rows(df)
    if len(duplicate_rows)>0:
        