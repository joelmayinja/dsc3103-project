#%%
import pandas as pd

import matplotlib.pyplot as plt

#%%
## here we import the rules from the rules.py file but can run from the terminal since its vs code
from src.validate import rules 


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


def price_histogram(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"].dropna(), bins=10, edgecolor="black")
    plt.title("Distribution of Commodity Prices")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("docs/price_histogram.png")
    plt.show()



 # Validation rules
    print("\nValidation failures:")
    print("Invalid prices:", len(rules.rule_positive_price(df)))
    print("Duplicate IDs:", len(rules.rule_duplicate_ids(df)))
    print("Duplicate rows:", len(rules.rule_duplicate_rows(df)))
    print("Invalid dates:", len(rules.rule_valid_date(df)))
    print("Missing markets:", len(rules.rule_missing_market(df)))
    print("Unknown commodities:", len(rules.rule_known_commodity(df)))

 



## This functions from the raw path. but it runs the rules on the data frame and prints them
def run_files(path = raw_path):
    ## reads the data frame from the path
    df = pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    negative_values(df)
    duplicate_ids(df)
    price_histogram(df)

## to run the fuction from the dataframe
if __name__ == "__main__":
    run_files("data/raw/prices.csv")


## to call and check if it works you say python src/validate/profile and it will print the schema of the data frame



   