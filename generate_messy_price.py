#%%
import csv
import random
from datetime import datetime, timedelta
# %%
random.seed(42)
base_date = datetime(2020, 1, 1)

rows = []

for i in range(1000):
    row = {
        "Id": i if random.random()>0.02 else i-1,
        "date": (base_date + timedelta(days=random.randint(0,1000))).strftime("%y-%m-%d") if random.random()>0.03 else "2020-14-50"



    }