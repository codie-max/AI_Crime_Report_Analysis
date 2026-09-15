import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "data/processed/cleaned_crime_reports.csv"


# Load cleaned dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("       EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print(f"\nTotal Records: {len(df)}")

# --------------------------------------------------
# 1. Crime Category Distribution
# --------------------------------------------------

category_counts = df["category"].value_counts()

print("\nCrime Category Distribution:")
print(category_counts)

plt.figure(figsize=(12, 7))
category_counts.sort_values().plot(kind="barh")

plt.title("Crime Category Distribution")
plt.xlabel("Number of Reports")
plt.ylabel("Crime Category")
plt.tight_layout()

plt.savefig("outputs/charts/crime_category_distribution.png")
plt.show()


# --------------------------------------------------
# 2. Top 10 Crime Subcategories
# --------------------------------------------------

subcategory_counts = df["sub_category"].value_counts().head(10)

print("\nTop 10 Crime Subcategories:")
print(subcategory_counts)

plt.figure(figsize=(12, 6))
subcategory_counts.sort_values().plot(kind="barh")

plt.title("Top 10 Crime Subcategories")
plt.xlabel("Number of Reports")
plt.ylabel("Crime Subcategory")
plt.tight_layout()

plt.savefig("outputs/charts/top_10_subcategories.png")
plt.show()


# --------------------------------------------------
# 3. Crime Report Length
# --------------------------------------------------

df["report_length"] = df["crimeaditionalinfo"].str.len()

print("\nCrime Report Length Statistics:")
print(df["report_length"].describe())

plt.figure(figsize=(10, 6))
plt.hist(df["report_length"], bins=50)

plt.title("Crime Report Length Distribution")
plt.xlabel("Report Length (Characters)")
plt.ylabel("Number of Reports")
plt.tight_layout()

plt.savefig("outputs/charts/report_length_distribution.png")
plt.show()


print("\n" + "=" * 60)
print("             EDA COMPLETE")
print("=" * 60)