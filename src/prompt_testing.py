import os
import json
import pandas as pd

from dotenv import load_dotenv
from google import genai

from prompts import CRIME_ANALYSIS_PROMPT


# ============================================================
# PROMPT QUALITY TESTING
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)

INPUT_FILE = "data/processed/cleaned_crime_reports.csv"


# ------------------------------------------------------------
# Load test records
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

test_df = df.head(5)

print("=" * 60)
print("             LLM PROMPT QUALITY TEST")
print("=" * 60)

print(f"\nTesting {len(test_df)} crime reports")


# ------------------------------------------------------------
# Expected fields
# ------------------------------------------------------------

expected_fields = [
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


successful = 0
missing_fields = 0


# ------------------------------------------------------------
# Test each report
# ------------------------------------------------------------

for index, row in test_df.iterrows():

    print("\n" + "-" * 60)
    print(f"Report {index + 1}")

    crime_report = str(row["crimeaditionalinfo"])

    prompt = CRIME_ANALYSIS_PROMPT.format(
        crime_report=crime_report
    )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        # Remove markdown formatting if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]

        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        analysis = json.loads(response_text)

        # Check required fields
        missing = [
            field
            for field in expected_fields
            if field not in analysis
        ]

        if not missing:

            successful += 1

            print("✓ All required fields present")

        else:

            missing_fields += 1

            print("✗ Missing fields:")
            print(missing)

        print("\nCrime Type:")
        print(analysis.get("crime_type"))

        print("\nSeverity:")
        print(analysis.get("severity"))

        print("\nLocation:")
        print(analysis.get("location"))

        print("\nFinancial Loss:")
        print(analysis.get("financial_loss"))

    except json.JSONDecodeError:

        missing_fields += 1

        print("✗ Invalid JSON returned by LLM")

    except Exception as e:

        missing_fields += 1

        print(f"✗ Error: {e}")


# ------------------------------------------------------------
# Final evaluation
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("             PROMPT TEST COMPLETE")
print("=" * 60)

print(f"\nReports tested: {len(test_df)}")
print(f"Reports with all required fields: {successful}")
print(f"Reports with missing/invalid output: {missing_fields}")

if successful == len(test_df):

    print("\n✓ PROMPT PASSED INITIAL QUALITY TEST")

else:

    print("\n⚠ PROMPT NEEDS IMPROVEMENT")

print("=" * 60)