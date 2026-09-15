import pandas as pd
from pathlib import Path


# ==========================================
# DAY 5 - CRIME TREND ANALYSIS
# ==========================================

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_crime_reports.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


# ==========================================
# LOAD DATA
# ==========================================

print("\n" + "=" * 60)
print("DAY 5 - CRIME TREND ANALYSIS")
print("=" * 60)

print("\nLoading cleaned crime report dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Total records: {len(df):,}")
print(f"Columns: {list(df.columns)}")


# ==========================================
# 1. CRIME CATEGORY ANALYSIS
# ==========================================

print("\n" + "-" * 60)
print("1. CRIME CATEGORY DISTRIBUTION")
print("-" * 60)

category_counts = (
    df["category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = ["category", "count"]

category_counts["percentage"] = (
    category_counts["count"] / len(df) * 100
).round(2)

print(category_counts.to_string(index=False))

category_counts.to_csv(
    OUTPUT_DIR / "crime_category_trends.csv",
    index=False
)


# ==========================================
# 2. SUBCATEGORY ANALYSIS
# ==========================================

print("\n" + "-" * 60)
print("2. TOP CRIME SUBCATEGORIES")
print("-" * 60)

subcategory_counts = (
    df["sub_category"]
    .value_counts()
    .head(15)
    .reset_index()
)

subcategory_counts.columns = ["sub_category", "count"]

subcategory_counts["percentage"] = (
    subcategory_counts["count"] / len(df) * 100
).round(2)

print(subcategory_counts.to_string(index=False))

subcategory_counts.to_csv(
    OUTPUT_DIR / "crime_subcategory_trends.csv",
    index=False
)


# ==========================================
# 3. REPORT LENGTH ANALYSIS
# ==========================================

print("\n" + "-" * 60)
print("3. CRIME REPORT LENGTH ANALYSIS")
print("-" * 60)

df["report_length"] = (
    df["crimeaditionalinfo"]
    .astype(str)
    .str.len()
)

length_statistics = pd.DataFrame({
    "metric": [
        "Total Reports",
        "Average Length",
        "Minimum Length",
        "Median Length",
        "Maximum Length"
    ],
    "value": [
        len(df),
        round(df["report_length"].mean(), 2),
        df["report_length"].min(),
        df["report_length"].median(),
        df["report_length"].max()
    ]
})

print(length_statistics.to_string(index=False))

length_statistics.to_csv(
    OUTPUT_DIR / "crime_report_length_statistics.csv",
    index=False
)


# ==========================================
# 4. MOST COMMON CRIME
# ==========================================

print("\n" + "-" * 60)
print("4. MOST COMMON CRIME CATEGORY")
print("-" * 60)

most_common_category = category_counts.iloc[0]

print(
    f"Most common category: {most_common_category['category']}"
)

print(
    f"Number of reports: {int(most_common_category['count']):,}"
)

print(
    f"Percentage of dataset: "
    f"{most_common_category['percentage']:.2f}%"
)


# ==========================================
# 5. MOST COMMON SUBCATEGORY
# ==========================================

print("\n" + "-" * 60)
print("5. MOST COMMON CRIME SUBCATEGORY")
print("-" * 60)

most_common_subcategory = subcategory_counts.iloc[0]

print(
    f"Most common subcategory: "
    f"{most_common_subcategory['sub_category']}"
)

print(
    f"Number of reports: "
    f"{int(most_common_subcategory['count']):,}"
)


# ==========================================
# SAVE SUMMARY
# ==========================================

summary = pd.DataFrame({
    "metric": [
        "Total Crime Reports",
        "Number of Crime Categories",
        "Most Common Crime Category",
        "Most Common Crime Category Count",
        "Most Common Crime Category Percentage",
        "Most Common Crime Subcategory",
        "Most Common Crime Subcategory Count"
    ],
    "value": [
        len(df),
        df["category"].nunique(),
        most_common_category["category"],
        int(most_common_category["count"]),
        most_common_category["percentage"],
        most_common_subcategory["sub_category"],
        int(most_common_subcategory["count"])
    ]
})

summary.to_csv(
    OUTPUT_DIR / "crime_trend_summary.csv",
    index=False
)


# ==========================================
# COMPLETE
# ==========================================

print("\n" + "=" * 60)
print("TREND ANALYSIS COMPLETE")
print("=" * 60)

print("\nGenerated files:")

print("✓ crime_category_trends.csv")
print("✓ crime_subcategory_trends.csv")
print("✓ crime_report_length_statistics.csv")
print("✓ crime_trend_summary.csv")

print("\nAll results saved in:")
print(OUTPUT_DIR)