import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


CATEGORY_FILE = PROCESSED_DIR / "crime_category_trends.csv"
SUBCATEGORY_FILE = PROCESSED_DIR / "crime_subcategory_trends.csv"
LENGTH_FILE = PROCESSED_DIR / "crime_report_length_statistics.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

category_df = pd.read_csv(CATEGORY_FILE)
subcategory_df = pd.read_csv(SUBCATEGORY_FILE)
length_df = pd.read_csv(LENGTH_FILE)


# ---------------------------------------------------------
# CATEGORY PATTERNS
# ---------------------------------------------------------

top_category = category_df.iloc[0]

top_5_categories = category_df.head(5).copy()

top_5_category_percentage = top_5_categories["percentage"].sum()


# ---------------------------------------------------------
# SUBCATEGORY PATTERNS
# ---------------------------------------------------------

top_subcategory = subcategory_df.iloc[0]

top_5_subcategories = subcategory_df.head(5).copy()

top_5_subcategory_percentage = top_5_subcategories["percentage"].sum()


# ---------------------------------------------------------
# REPORT LENGTH
# ---------------------------------------------------------

length_stats = dict(
    zip(length_df["metric"], length_df["value"])
)

total_reports = int(length_stats["Total Reports"])
average_length = float(length_stats["Average Length"])
median_length = float(length_stats["Median Length"])
maximum_length = int(length_stats["Maximum Length"])


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("=" * 60)
print("DAY 7 - CRIME PATTERN ANALYSIS")
print("=" * 60)

print("\nDataset Overview")
print("-" * 60)
print(f"Total Reports: {total_reports:,}")
print(f"Total Crime Categories: {len(category_df):,}")
print(f"Total Crime Subcategories: {len(subcategory_df):,}")


print("\nDominant Crime Category")
print("-" * 60)
print(f"Category: {top_category['category']}")
print(f"Count: {int(top_category['count']):,}")
print(f"Percentage: {top_category['percentage']:.2f}%")


print("\nDominant Crime Subcategory")
print("-" * 60)
print(f"Subcategory: {top_subcategory['sub_category']}")
print(f"Count: {int(top_subcategory['count']):,}")
print(f"Percentage: {top_subcategory['percentage']:.2f}%")


print("\nTop 5 Crime Categories")
print("-" * 60)

for _, row in top_5_categories.iterrows():
    print(
        f"{row['category']}: "
        f"{int(row['count']):,} "
        f"({row['percentage']:.2f}%)"
    )


print(f"\nCombined percentage of Top 5 Categories: "
      f"{top_5_category_percentage:.2f}%")


print("\nTop 5 Crime Subcategories")
print("-" * 60)

for _, row in top_5_subcategories.iterrows():
    print(
        f"{row['sub_category']}: "
        f"{int(row['count']):,} "
        f"({row['percentage']:.2f}%)"
    )


print(f"\nCombined percentage of Top 5 Subcategories: "
      f"{top_5_subcategory_percentage:.2f}%")


print("\nCrime Report Length Pattern")
print("-" * 60)
print(f"Average Report Length: {average_length:.2f} characters")
print(f"Median Report Length: {median_length:.0f} characters")
print(f"Maximum Report Length: {maximum_length:,} characters")


print("\nKey Pattern Findings")
print("-" * 60)

print(
    f"1. {top_category['category']} is the most frequently reported "
    f"crime category, representing {top_category['percentage']:.2f}% "
    f"of the cleaned dataset."
)

print(
    f"2. {top_subcategory['sub_category']} is the most frequently "
    f"reported subcategory, representing "
    f"{top_subcategory['percentage']:.2f}% of the dataset."
)

print(
    f"3. The top five crime categories together account for "
    f"{top_5_category_percentage:.2f}% of all reports."
)

print(
    f"4. The average crime report contains approximately "
    f"{average_length:.0f} characters, while the median is "
    f"{median_length:.0f} characters."
)

print(
    "\nNote: The dataset does not contain a dedicated date field. "
    "Therefore, the findings represent crime distributions and "
    "patterns rather than chronological trends over time."
)

print("\n" + "=" * 60)
print("PATTERN ANALYSIS COMPLETE")
print("=" * 60)