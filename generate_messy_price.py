#%%
import csv
import random
from datetime import datetime, timedelta
# %%
random.seed(42)
base_date = datetime(2020, 1, 1)

markets = ["Mukono" , "Bwaise" , "Nakasero" , "Kasanga" , None]

Commodities = ["Maize", "MAIZE" , "Beans" , "BEANS" ,  ]

rows = []

for i in range(1000):
    row = {
        "Id": i if random.random()>0.02 else i-1,
        "date": (base_date + timedelta(days=random.randint(0,1000))).strftime("%y-%m-%d") if random.random()>0.03 else "2020-14-50",
        "markets" : random.choice (markets) ,
        "Comodities" : random.choice (Commodities),
        "price" : random.randint(500,5000) if random.random() > 0.05 else -2000
    }

    rows.append(row)

rows += rows[20:30]

with open("data/raw/prices.csv", "w" , newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Id","date", "markets", "Comodities",  "price"])
    writer.writeheader()
    writer.writerows(rows)
#%%
