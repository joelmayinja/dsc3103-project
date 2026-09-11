#%%
import pandas as pd
from src.common.config import SOURCE_A_RAW_PATH  #Here we are importing it from the config file, so that if changes are made to the source path, we can change it in one place and it will be reflected throughout the code.

def ingest_source_a(path =SOURCE_A_RAW_PATH):
    df = pd.read_csv(path)
    return df
# %%
## this is what we call hard coding above, we can make it more flexible by passing the path as an argument to the function.
#This is done better by storing a source path so that if chsanges are made to the source path, we can change it in one place and it will be reflected throughout the code.