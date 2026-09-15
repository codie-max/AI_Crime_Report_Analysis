import pandas as pd

DATA_PATH = "data/processed/cleaned_crime_reports.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("       CLEANED CRIME DATASET VALIDATION")
print("=" * 60)

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Columns:")
print(df.columns.tolist())

print("\n3. Missing Values:")
print(df.isnull().sum())

print("\n4. Duplicate Records:")
print(df.duplicated().sum())

print("\n5. Crime Categories:")
print(df["category"].value_counts())

print("\n6. Top 10 Subcategories:")
print(df["sub_category"].value_counts().head(10))

print("\n7. Sample Crime Reports:")
for i, report in enumerate(df["crimeaditionalinfo"].head(5), start=1):
    print(f"\nReport {i}:")
    print(report)

print("\n" + "=" * 60)
print("          VALIDATION COMPLETE")
print("=" * 60)