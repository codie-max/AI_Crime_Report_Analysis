import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --------------------------------
# LOAD ANALYSIS FILES
# --------------------------------

category_df = pd.read_csv(
    PROCESSED_DIR / "crime_category_trends.csv"
)

subcategory_df = pd.read_csv(
    PROCESSED_DIR / "crime_subcategory_trends.csv"
)

length_df = pd.read_csv(
    PROCESSED_DIR / "crime_report_length_statistics.csv"
)

llm_severity_df = pd.read_csv(
    PROCESSED_DIR / "llm_severity_distribution.csv"
)

llm_crime_df = pd.read_csv(
    PROCESSED_DIR / "llm_crime_type_distribution.csv"
)

print("\n" + "=" * 60)
print("DAY 5 - TREND & INSIGHT REPORT")
print("=" * 60)

# --------------------------------
# FULL DATASET
# --------------------------------

total_records = int(category_df["count"].sum())

top_category = category_df.iloc[0]
top_subcategory = subcategory_df.iloc[0]

# Get report length values safely
print("\nReport length statistics:")
print(length_df)

# Detect the column containing the values
average_length = float(
    length_df.loc[
        length_df["metric"] == "Average Length",
        "value"
    ].iloc[0]
)

median_length = float(
    length_df.loc[
        length_df["metric"] == "Median Length",
        "value"
    ].iloc[0]
)


print("\n1. FULL DATASET INSIGHTS")
print("-" * 40)

print(
    f"• The dataset contains {total_records:,} cleaned crime reports."
)

print(
    f"• The most common crime category is "
    f"{top_category['category']} with "
    f"{int(top_category['count']):,} reports "
    f"({top_category['percentage']:.2f}%)."
)

print(
    f"• The most common subcategory is "
    f"{top_subcategory['sub_category']} with "
    f"{int(top_subcategory['count']):,} reports "
    f"({top_subcategory['percentage']:.2f}%)."
)

print(
    f"• The average crime report length is "
    f"{average_length:.2f} characters."
)

print(
    f"• The median crime report length is "
    f"{median_length:.0f} characters."
)

# --------------------------------
# LLM SAMPLE
# --------------------------------

llm_total = int(llm_severity_df["count"].sum())

high_severity = llm_severity_df[
    llm_severity_df["severity"].astype(str).str.lower() == "high"
]

high_count = (
    int(high_severity["count"].iloc[0])
    if not high_severity.empty
    else 0
)

high_percentage = (
    high_count / llm_total * 100
    if llm_total > 0
    else 0
)

print("\n2. LLM-BASED SAMPLE INSIGHTS")
print("-" * 40)

print(
    f"• The initial LLM analysis sample contains "
    f"{llm_total} successfully analyzed reports."
)

print(
    f"• {high_count} reports were classified as High severity "
    f"({high_percentage:.2f}% of the LLM sample)."
)

print(
    "• The LLM extracted structured information such as "
    "crime type, modus operandi, platforms, entities, "
    "location, temporal information, financial loss, and severity."
)

# --------------------------------
# ANALYTICAL NOTE
# --------------------------------

print("\n3. IMPORTANT ANALYTICAL NOTE")
print("-" * 40)

print(
    "• The current dataset does not contain a dedicated date column."
)

print(
    "• Therefore, the current analysis represents crime "
    "distributions and patterns rather than trends over time."
)

print(
    f"• LLM-based percentages are based only on the initial "
    f"{llm_total}-report sample and should not be generalized "
    "to the complete dataset."
)

# --------------------------------
# SAVE REPORT
# --------------------------------

report_lines = [
    "CRIME REPORT ANALYSIS - TREND & INSIGHT REPORT",
    "=" * 55,
    "",
    "1. FULL DATASET INSIGHTS",
    "",
    f"The dataset contains {total_records:,} cleaned crime reports.",
    f"The most common crime category is "
    f"{top_category['category']} with "
    f"{int(top_category['count']):,} reports "
    f"({top_category['percentage']:.2f}%).",
    f"The most common subcategory is "
    f"{top_subcategory['sub_category']} with "
    f"{int(top_subcategory['count']):,} reports "
    f"({top_subcategory['percentage']:.2f}%).",
    f"The average crime report length is "
    f"{average_length:.2f} characters.",
    f"The median crime report length is "
    f"{median_length:.0f} characters.",
    "",
    "2. LLM-BASED SAMPLE INSIGHTS",
    "",
    f"The initial LLM analysis sample contains "
    f"{llm_total} successfully analyzed reports.",
    f"{high_count} reports were classified as High severity "
    f"({high_percentage:.2f}% of the LLM sample).",
    "The LLM extracted structured information including "
    "crime type, modus operandi, platforms, entities, "
    "location, temporal information, financial loss, and severity.",
    "",
    "3. IMPORTANT ANALYTICAL NOTE",
    "",
    "The current dataset does not contain a dedicated date column.",
    "Therefore, the current analysis represents crime distributions "
    "and patterns rather than trends over time.",
    f"LLM-based percentages are based only on the initial "
    f"{llm_total}-report sample and should not be generalized "
    "to the complete dataset."
]

output_file = PROCESSED_DIR / "crime_trend_insight_report.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("\n" + "=" * 60)
print("✓ Insight report saved to:")
print(output_file)
print("=" * 60)