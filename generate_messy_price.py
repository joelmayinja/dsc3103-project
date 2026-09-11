import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
base_date = datetime(2020, 1, 1)
markets = ["Mukono", "Bwaise", "Nakasero", "Kasanga", None]
commodities = ["Maize", "MAIZE", "maize ", "Beans", "BEANS", "Beans "]

rows = []
for i in range(1000):
    record_id = i if random.random() > 0.02 else max(i - 1, 0)
    date_value = (base_date + timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")
    if random.random() < 0.03:
        date_value = "2020-14-50"
    price_value = random.randint(500, 5000) if random.random() > 0.05 else -2000
    row = {
        "record_id": record_id,
        "date": date_value,
        "market": random.choice(markets),
        "commodity": random.choice(commodities),
        "price": price_value,
    }
    rows.append(row)

for row in rows[20:30]:
    rows.append(dict(row))

output_path = Path(__file__).resolve().parent / "data" / "raw" / "prices.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["record_id", "date", "market", "commodity", "price"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows in {output_path}")
