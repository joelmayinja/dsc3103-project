#%%
import pandas as pd

#%%
## here we import the rules from the rules.py file but can run from the terminal since its vs code
from scr.validate import rules 
raw_path = "data/raw/prices.csv"

## this is the main function that will run the rules on the data
def inferred_schema(df):
    print("\n---- Inferred Schema ----")
    print("----------------------------")
    print(df.dtypes)

def row_count(df):
         print("\n---- Row Count ----")
         print("----------------------------")
         print(len(df))

## this function will run the rules on the data frame and print the number of negative values
def negative_values(df):
     negative_values = rules.rule_positive_price(df)
     print("\n---- Negative Values ----")
     print("----------------------------")
     print(len(negative_values))

def duplicate_ids(df):
     duplicate_ids = rules.rule_duplicate_ids(df)
     print("\n---- Duplicate IDs ----")
     print("----------------------------")
     print(len(duplicate_ids))


## This functions from the raw path. but it runs the rules on the data frame and prints them
def run_files(path = raw_path):
    ## reads the data frame from the path
    df = pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    negative_values(df)
    duplicate_ids(df)
## to run the fuction from the dataframe
if __name__ == "__main__":
    run_files()

## to call and check if it works you say python scr/validate/profile and it will print the schema of the data frame

