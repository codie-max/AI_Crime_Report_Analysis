import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# DAY 5 - CRIME TREND VISUALIZATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CHART_DIR = DATA_DIR / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)


print("\n" + "=" * 60)
print("DAY 5 - CRIME TREND VISUALIZATION")
print("=" * 60)


# ==========================================
# 1. CRIME CATEGORY DISTRIBUTION
# ==========================================

category_path = DATA_DIR / "crime_category_trends.csv"
category_df = pd.read_csv(category_path)

plt.figure(figsize=(12, 7))

plt.barh(
    category_df["category"],
    category_df["count"]
)

plt.xlabel("Number of Reports")
plt.ylabel("Crime Category")
plt.title("Crime Category Distribution")

plt.gca().invert_yaxis()

plt.tight_layout()

category_chart = CHART_DIR / "crime_category_distribution.png"
plt.savefig(category_chart, dpi=300)
plt.close()

print("\n✓ Crime category chart saved")


# ==========================================
# 2. TOP 10 SUBCATEGORIES
# ==========================================

subcategory_path = DATA_DIR / "crime_subcategory_trends.csv"
subcategory_df = pd.read_csv(subcategory_path)

top_subcategories = subcategory_df.head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    top_subcategories["sub_category"],
    top_subcategories["count"]
)

plt.xlabel("Number of Reports")
plt.ylabel("Crime Subcategory")
plt.title("Top 10 Crime Subcategories")

plt.gca().invert_yaxis()

plt.tight_layout()

subcategory_chart = CHART_DIR / "top_crime_subcategories.png"
plt.savefig(subcategory_chart, dpi=300)
plt.close()

print("✓ Subcategory chart saved")


# ==========================================
# 3. LLM SEVERITY DISTRIBUTION
# ==========================================

severity_path = DATA_DIR / "llm_severity_distribution.csv"
severity_df = pd.read_csv(severity_path)

plt.figure(figsize=(8, 6))

plt.bar(
    severity_df["severity"],
    severity_df["count"]
)

plt.xlabel("Severity")
plt.ylabel("Number of Reports")
plt.title("LLM-Based Severity Distribution")

plt.tight_layout()

severity_chart = CHART_DIR / "llm_severity_distribution.png"
plt.savefig(severity_chart, dpi=300)
plt.close()

print("✓ Severity chart saved")


# ==========================================
# 4. LLM CRIME TYPE DISTRIBUTION
# ==========================================

crime_type_path = DATA_DIR / "llm_crime_type_distribution.csv"
crime_type_df = pd.read_csv(crime_type_path)

plt.figure(figsize=(12, 7))

plt.barh(
    crime_type_df["crime_type"],
    crime_type_df["count"]
)

plt.xlabel("Number of Reports")
plt.ylabel("LLM-Identified Crime Type")
plt.title("LLM-Identified Crime Types")

plt.gca().invert_yaxis()

plt.tight_layout()

crime_type_chart = CHART_DIR / "llm_crime_type_distribution.png"
plt.savefig(crime_type_chart, dpi=300)
plt.close()

print("✓ LLM crime type chart saved")


# ==========================================
# COMPLETE
# ==========================================

print("\n" + "=" * 60)
print("TREND VISUALIZATION COMPLETE")
print("=" * 60)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nGenerated charts:")
print("✓ crime_category_distribution.png")
print("✓ top_crime_subcategories.png")
print("✓ llm_severity_distribution.png")
print("✓ llm_crime_type_distribution.png")