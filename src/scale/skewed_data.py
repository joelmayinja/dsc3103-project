import numpy as np
import pandas as pd

SRC = "data/processed/prices_with_rainfall.parquet"
OUT = "data/processed/prices_skewed.parquet"
N_ROWS = 5_000_000

def skewed_data():
    base = pd.read_parquet(SRC)
    rng = np.random.default_rng(42)

    # Sample rows from the prices_with_rainfall data 
    big = base.sample(n=N_ROWS, replace=True, random_state=42).reset_index(drop=True)

    # Make the data skewed(70% to belong to "Owino")
    skewed = rng.random(N_ROWS) < 0.70
    big.loc[skewed, "market"] = "Owino"

    big["id"] = np.arange(N_ROWS)

    big.to_parquet(OUT, index=False)
    print(big["market"].value_counts(normalize=True).round(3))
    print("Wrote", OUT, "rows:", len(big))

if __name__ == "__main__":
    skewed_data()