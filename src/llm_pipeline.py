import os
import json
import time
import pandas as pd

from dotenv import load_dotenv
from google import genai

from prompts import CRIME_ANALYSIS_PROMPT


# ============================================================
# LLM CRIME ANALYSIS PIPELINE
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)

INPUT_FILE = "data/processed/cleaned_crime_reports.csv"
OUTPUT_FILE = "data/processed/llm_pipeline_test.csv"


# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# TEST MODE:
# Process only 5 reports for now.
TEST_LIMIT = 5

test_df = df.head(TEST_LIMIT).copy()

print("=" * 60)
print("           LLM CRIME ANALYSIS PIPELINE")
print("=" * 60)

print(f"\nTotal reports available: {len(df)}")
print(f"Reports selected for testing: {len(test_df)}")


# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

def clean_json_response(response_text):

    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    return response_text.strip()


# ------------------------------------------------------------
# Process reports
# ------------------------------------------------------------

results = []

for index, row in test_df.iterrows():

    print("\n" + "-" * 60)
    print(f"Processing report {index + 1}/{len(test_df)}")

    crime_report = str(row["crimeaditionalinfo"])

    prompt = CRIME_ANALYSIS_PROMPT.format(
        crime_report=crime_report
    )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = clean_json_response(response.text)

        # Convert LLM JSON into Python dictionary
        analysis = json.loads(response_text)

        # Preserve original dataset information
        analysis["report_id"] = index
        analysis["category"] = row["category"]
        analysis["sub_category"] = row["sub_category"]

        results.append(analysis)

        print("✓ LLM analysis successful")

    except json.JSONDecodeError:

        print("✗ Invalid JSON returned by LLM")

        results.append({
            "report_id": index,
            "category": row["category"],
            "sub_category": row["sub_category"],
            "crime_type": "Unknown",
            "summary": "Analysis unavailable",
            "modus_operandi": "Analysis unavailable",
            "platforms": [],
            "entities": [],
            "location": None,
            "temporal_information": None,
            "financial_loss": "Not specified",
            "severity": "Unknown"
        })

    except Exception as e:

        print(f"✗ API/processing error: {e}")

        results.append({
            "report_id": index,
            "category": row["category"],
            "sub_category": row["sub_category"],
            "crime_type": "Unknown",
            "summary": "Analysis unavailable",
            "modus_operandi": "Analysis unavailable",
            "platforms": [],
            "entities": [],
            "location": None,
            "temporal_information": None,
            "financial_loss": "Not specified",
            "severity": "Unknown"
        })

    # Small delay between requests
    time.sleep(1)


# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

results_df = pd.DataFrame(results)


# ------------------------------------------------------------
# Validate expected columns
# ------------------------------------------------------------

expected_columns = [
    "report_id",
    "category",
    "sub_category",
    "crime_type",
    "summary",
    "modus_operandi",
    "platforms",
    "entities",
    "location",
    "temporal_information",
    "financial_loss",
    "severity"
]

for column in expected_columns:

    if column not in results_df.columns:
        results_df[column] = None

results_df = results_df[expected_columns]


# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("             PIPELINE TEST COMPLETE")
print("=" * 60)

print(f"\nSuccessful/processed records: {len(results_df)}")

print("\nSeverity distribution:")

print(
    results_df["severity"]
    .value_counts(dropna=False)
)

print("\nCrime types detected:")

print(
    results_df["crime_type"]
    .value_counts(dropna=False)
)

print("\nResults saved to:")

print(OUTPUT_FILE)

print("=" * 60)