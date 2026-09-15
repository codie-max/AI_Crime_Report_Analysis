import pandas as pd
from pathlib import Path


# ==========================================
# DAY 5 - LLM TREND ANALYSIS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "llm_batch_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


print("\n" + "=" * 60)
print("DAY 5 - LLM-BASED INSIGHT ANALYSIS")
print("=" * 60)


# ==========================================
# LOAD LLM RESULTS
# ==========================================

df = pd.read_csv(INPUT_PATH)

# Keep only successfully processed records
df = df[df["processing_status"] == "success"].copy()

print(f"\nSuccessfully analyzed reports: {len(df)}")


# ==========================================
# 1. CRIME TYPE DISTRIBUTION
# ==========================================

print("\n" + "-" * 60)
print("1. LLM-IDENTIFIED CRIME TYPES")
print("-" * 60)

crime_types = (
    df["crime_type"]
    .value_counts()
    .reset_index()
)

crime_types.columns = ["crime_type", "count"]

crime_types["percentage"] = (
    crime_types["count"] / len(df) * 100
).round(2)

print(crime_types.to_string(index=False))

crime_types.to_csv(
    OUTPUT_DIR / "llm_crime_type_distribution.csv",
    index=False
)


# ==========================================
# 2. SEVERITY DISTRIBUTION
# ==========================================

print("\n" + "-" * 60)
print("2. SEVERITY DISTRIBUTION")
print("-" * 60)

severity = (
    df["severity"]
    .value_counts()
    .reset_index()
)

severity.columns = ["severity", "count"]

severity["percentage"] = (
    severity["count"] / len(df) * 100
).round(2)

print(severity.to_string(index=False))

severity.to_csv(
    OUTPUT_DIR / "llm_severity_distribution.csv",
    index=False
)


# ==========================================
# 3. LOCATION INFORMATION
# ==========================================

print("\n" + "-" * 60)
print("3. LOCATION EXTRACTION")
print("-" * 60)

location_available = (
    df["location"]
    .notna()
    & (df["location"].astype(str).str.strip() != "")
    & (df["location"].astype(str).str.lower() != "none")
)

location_count = location_available.sum()

print(f"Reports with location information: {location_count}")
print(
    f"Reports without location information: "
    f"{len(df) - location_count}"
)


# ==========================================
# 4. FINANCIAL LOSS INFORMATION
# ==========================================

print("\n" + "-" * 60)
print("4. FINANCIAL LOSS INFORMATION")
print("-" * 60)

financial_loss_available = (
    df["financial_loss"]
    .notna()
    & (
        df["financial_loss"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin([
            "",
            "none",
            "not specified",
            "not mentioned",
            "unknown"
        ])
        == False
    )
)

financial_loss_count = financial_loss_available.sum()

print(
    f"Reports containing financial-loss information: "
    f"{financial_loss_count}"
)

print("\nFinancial-loss values:")

if financial_loss_count > 0:
    print(
        df.loc[
            financial_loss_available,
            ["report_id", "financial_loss"]
        ].to_string(index=False)
    )
else:
    print("No financial-loss information identified.")


# ==========================================
# 5. PLATFORM INFORMATION
# ==========================================

print("\n" + "-" * 60)
print("5. PLATFORM INFORMATION")
print("-" * 60)

platform_values = []

for value in df["platforms"].dropna():

    value = str(value).strip()

    if value and value.lower() not in ["none", "[]"]:
        platform_values.append(value)

print(f"Reports containing platform information: {len(platform_values)}")

for platform in platform_values:
    print(f"- {platform}")


# ==========================================
# 6. GENERATE SUMMARY
# ==========================================

most_common_crime = crime_types.iloc[0]["crime_type"]
most_common_crime_count = int(crime_types.iloc[0]["count"])

most_common_severity = severity.iloc[0]["severity"]
most_common_severity_count = int(severity.iloc[0]["count"])


summary = pd.DataFrame({
    "metric": [
        "LLM Analyzed Reports",
        "Most Common LLM Crime Type",
        "Most Common Crime Type Count",
        "Most Common Severity",
        "Most Common Severity Count",
        "Reports With Location",
        "Reports With Financial Loss"
    ],
    "value": [
        len(df),
        most_common_crime,
        most_common_crime_count,
        most_common_severity,
        most_common_severity_count,
        location_count,
        financial_loss_count
    ]
})


summary.to_csv(
    OUTPUT_DIR / "llm_trend_summary.csv",
    index=False
)


# ==========================================
# COMPLETE
# ==========================================

print("\n" + "=" * 60)
print("LLM TREND ANALYSIS COMPLETE")
print("=" * 60)

print("\nGenerated files:")
print("✓ llm_crime_type_distribution.csv")
print("✓ llm_severity_distribution.csv")
print("✓ llm_trend_summary.csv")

print("\nResults saved to:")
print(OUTPUT_DIR)