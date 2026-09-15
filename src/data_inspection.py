import pandas as pd

# Path to the raw dataset
DATA_PATH = "data/raw/train.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("       CRIME REPORT DATASET INSPECTION")
print("=" * 60)

# Basic information
print("\n1. Dataset Shape:")
print(df.shape)

# Column names
print("\n2. Columns:")
print(df.columns.tolist())

# First 5 records
print("\n3. First 5 Records:")
print(df.head())

# Data types
print("\n4. Data Types:")
print(df.dtypes)

# Missing values
print("\n5. Missing Values:")
print(df.isnull().sum())

# Duplicate records
print("\n6. Duplicate Records:")
print(df.duplicated().sum())

# Crime categories
if "category" in df.columns:
    print("\n7. Crime Categories:")
    print(df["category"].value_counts())

# Crime subcategories
if "sub_category" in df.columns:
    print("\n8. Crime Subcategories:")
    print(df["sub_category"].value_counts().head(20))

# Report text statistics
if "crimeaditionalinfo" in df.columns:
    df["report_length"] = df["crimeaditionalinfo"].astype(str).str.len()

    print("\n9. Report Text Statistics:")
    print(df["report_length"].describe())

print("\n" + "=" * 60)
print("             INSPECTION COMPLETE")
print("=" * 60)