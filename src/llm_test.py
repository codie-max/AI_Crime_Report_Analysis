import os
import json
import pandas as pd

from dotenv import load_dotenv
from google import genai

from prompts import CRIME_ANALYSIS_PROMPT


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )


# --------------------------------------------------
# 2. Initialize Gemini
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# 3. Load cleaned dataset
# --------------------------------------------------

DATA_PATH = "data/processed/cleaned_crime_reports.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("       LLM STRUCTURED CRIME ANALYSIS")
print("=" * 60)

print(f"\nTotal reports in dataset: {len(df)}")


# --------------------------------------------------
# 4. Analyze first 5 reports
# --------------------------------------------------

results = []

for i in range(5):

    crime_report = df.loc[i, "crimeaditionalinfo"]

    prompt = CRIME_ANALYSIS_PROMPT.format(
        crime_report=crime_report
    )

    print(f"\nAnalyzing report {i + 1}/5...")

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if response_text.startswith("```json"):
            response_text = response_text[7:]

        if response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        # Convert JSON string into Python dictionary
        analysis = json.loads(response_text)

        # Add original dataset information
        analysis["category"] = df.loc[i, "category"]
        analysis["sub_category"] = df.loc[i, "sub_category"]
        analysis["report_id"] = i

        results.append(analysis)

        print("✓ Successfully analyzed")

    except Exception as e:

        print(f"✗ Error analyzing report {i + 1}: {e}")


# --------------------------------------------------
# 5. Convert results to DataFrame
# --------------------------------------------------

results_df = pd.DataFrame(results)


# --------------------------------------------------
# 6. Display structured results
# --------------------------------------------------

print("\n" + "=" * 60)
print("             STRUCTURED RESULTS")
print("=" * 60)

if not results_df.empty:

    print("\nColumns:")
    print(results_df.columns.tolist())

    print("\nStructured Crime Records:")

    print(
        results_df[
            [
                "report_id",
                "category",
                "sub_category",
                "crime_type",
                "summary",
                "modus_operandi",
                "platforms",
                "location",
                "financial_loss",
                "severity"
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 7. Save structured results
# --------------------------------------------------

OUTPUT_PATH = "data/processed/llm_structured_crime_records.csv"

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n" + "=" * 60)
print("STRUCTURED CRIME RECORDS SAVED")
print("=" * 60)

print(f"\nSaved to:")
print(OUTPUT_PATH)

print(f"\nRecords processed: {len(results_df)}")