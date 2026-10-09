import pandas as pd

results = pd.read_csv("data/raw/results.csv")
races = pd.read_csv("data/raw/races.csv")
drivers = pd.read_csv("data/raw/drivers.csv")

print("RESULTS")
print(results.head())
print("\nColonne:", results.columns.tolist())

print("\nRACES")
print(races.head())
print("\nColonne:", races.columns.tolist())

print("\nDRIVERS")
print(drivers.head())
print("\nColonne:", drivers.columns.tolist())
