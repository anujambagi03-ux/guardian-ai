import pandas as pd
import numpy as np

np.random.seed(42)

records = 5000

data = {
    "hour": np.random.randint(0, 24, records),
    "day_of_week": np.random.randint(0, 7, records),
    "traffic_density": np.random.randint(10, 100, records),
    "rainfall": np.random.randint(0, 100, records),
    "visibility": np.random.randint(10, 100, records),
    "speed_avg": np.random.randint(20, 120, records),
    "junction_score": np.random.randint(1, 10, records),
    "accident_risk": np.random.randint(0, 2, records)
}

df = pd.DataFrame(data)

df.to_csv(
    "../datasets/accident_risk_dataset.csv",
    index=False
)

print("Dataset generated successfully.")
print(df.head())