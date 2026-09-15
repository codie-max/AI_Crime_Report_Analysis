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

OUTPUT_FILE = PROCESSED_DIR / "crime_pattern_insights.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

category_df = pd.read_csv(CATEGORY_FILE)
subcategory_df = pd.read_csv(SUBCATEGORY_FILE)
length_df = pd.read_csv(LENGTH_FILE)


# ---------------------------------------------------------
# EXTRACT STATISTICS
# ---------------------------------------------------------

top_category = category_df.iloc[0]
top_subcategory = subcategory_df.iloc[0]

top_5_category_percentage = category_df.head(5)["percentage"].sum()

length_stats = dict(
    zip(length_df["metric"], length_df["value"])
)

total_reports = int(length_stats["Total Reports"])
average_length = float(length_stats["Average Length"])
median_length = float(length_stats["Median Length"])


# ---------------------------------------------------------
# GENERATE INSIGHTS
# ---------------------------------------------------------

insights = [

    {
        "insight_type": "Dominant Category",
        "finding": (
            f"{top_category['category']} is the most frequently reported "
            f"crime category, accounting for "
            f"{top_category['percentage']:.2f}% of all reports."
        )
    },

    {
        "insight_type": "Dominant Subcategory",
        "finding": (
            f"{top_subcategory['sub_category']} is the most frequently "
            f"reported crime subcategory, accounting for "
            f"{top_subcategory['percentage']:.2f}% of all reports."
        )
    },

    {
        "insight_type": "Category Concentration",
        "finding": (
            f"The top five crime categories together represent "
            f"{top_5_category_percentage:.2f}% of the dataset, "
            f"indicating a strong concentration of reported incidents "
            f"within a small number of crime categories."
        )
    },

    {
        "insight_type": "Report Length",
        "finding": (
            f"Crime reports contain an average of approximately "
            f"{average_length:.0f} characters, while the median report "
            f"length is {median_length:.0f} characters."
        )
    },

    {
        "insight_type": "Dataset Scope",
        "finding": (
            f"The analysis covers {total_reports:,} cleaned crime reports "
            f"across {len(category_df)} crime categories. The dataset "
            f"does not contain a dedicated date field, so the analysis "
            f"identifies distributions and patterns rather than "
            f"chronological crime trends."
        )
    }
]


# ---------------------------------------------------------
# SAVE INSIGHTS
# ---------------------------------------------------------

insights_df = pd.DataFrame(insights)

insights_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("=" * 60)
print("DAY 7 - INSIGHT GENERATION")
print("=" * 60)

print(f"\nGenerated {len(insights_df)} analytical insights.\n")

for _, row in insights_df.iterrows():
    print(f"[{row['insight_type']}]")
    print(row["finding"])
    print()

print(f"Output saved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("INSIGHT GENERATION COMPLETE")
print("=" * 60)