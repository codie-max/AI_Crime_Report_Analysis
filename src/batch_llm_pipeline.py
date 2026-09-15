import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

from prompts import CRIME_ANALYSIS_PROMPT


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/cleaned_crime_reports.csv"
OUTPUT_FILE = "data/processed/llm_batch_results.csv"

TEST_LIMIT = 10

MODEL_NAME = "gemini-2.5-flash"

# Gemini free-tier safety
SLEEP_SECONDS = 15


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )


# ============================================================
# INITIALIZE GEMINI
# ============================================================

client = genai.Client(api_key=API_KEY)


# ============================================================
# CLEAN JSON RESPONSE
# ============================================================

def clean_json_response(text):

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ============================================================
# ANALYZE ONE REPORT
# ============================================================

def analyze_report(report_id, report_text):

    try:

        prompt = CRIME_ANALYSIS_PROMPT.format(
            crime_report=report_text
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        cleaned_response = clean_json_response(
            response.text
        )

        result = json.loads(cleaned_response)

        result["report_id"] = report_id
        result["processing_status"] = "success"
        result["error"] = None

        return result

    except Exception as e:

        return {
            "report_id": report_id,
            "crime_type": None,
            "summary": None,
            "modus_operandi": None,
            "platforms": [],
            "entities": [],
            "location": None,
            "temporal_information": None,
            "financial_loss": None,
            "severity": None,
            "processing_status": "failed",
            "error": str(e)
        }


# ============================================================
# SAVE CLEAN CHECKPOINT
# ============================================================

def save_checkpoint(existing_results, new_results):

    new_df = pd.DataFrame(new_results)

    if existing_results.empty:

        combined = new_df

    else:

        combined = pd.concat(
            [
                existing_results,
                new_df
            ],
            ignore_index=True
        )

    # --------------------------------------------------------
    # Keep the latest result for each report_id
    # --------------------------------------------------------

    combined = combined.drop_duplicates(
        subset=["report_id"],
        keep="last"
    )

    # --------------------------------------------------------
    # Sort by report ID
    # --------------------------------------------------------

    combined["report_id"] = (
        combined["report_id"]
        .astype(str)
    )

    combined = combined.sort_values(
        by="report_id",
        key=lambda x: x.astype(int)
    )

    combined.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return combined


# ============================================================
# MAIN PIPELINE
# ============================================================

print("=" * 60)
print("             RESUMABLE LLM BATCH PIPELINE")
print("=" * 60)


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Total reports available: {len(df)}"
)


# ============================================================
# SELECT TEST DATA
# ============================================================

working_df = df.head(TEST_LIMIT).copy()

working_df["report_id"] = (
    working_df.index.astype(str)
)

print(
    f"Reports selected for this run: "
    f"{len(working_df)}"
)


# ============================================================
# LOAD EXISTING CHECKPOINT
# ============================================================

if os.path.exists(OUTPUT_FILE):

    print("\nExisting checkpoint found.")

    existing_results = pd.read_csv(
        OUTPUT_FILE
    )

    # --------------------------------------------------------
    # CLEAN OLD DUPLICATES
    # --------------------------------------------------------

    existing_results["report_id"] = (
        existing_results["report_id"]
        .astype(str)
    )

    existing_results = existing_results.drop_duplicates(
        subset=["report_id"],
        keep="last"
    )

    existing_results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Clean checkpoint records: "
        f"{len(existing_results)}"
    )

else:

    print("\nNo previous checkpoint found.")

    existing_results = pd.DataFrame()


# ============================================================
# FIND SUCCESSFULLY PROCESSED REPORTS
# ============================================================

if not existing_results.empty:

    successful_ids = set(
        existing_results.loc[
            existing_results["processing_status"] == "success",
            "report_id"
        ].astype(str)
    )

else:

    successful_ids = set()


print(
    f"Successfully processed previously: "
    f"{len(successful_ids)}"
)


# ============================================================
# FIND REMAINING REPORTS
# ============================================================

remaining_df = working_df[
    ~working_df["report_id"].isin(successful_ids)
].copy()


print(
    f"Reports remaining/requiring retry: "
    f"{len(remaining_df)}"
)


# ============================================================
# PROCESS REMAINING REPORTS
# ============================================================

if len(remaining_df) == 0:

    print(
        "\nAll selected reports have already "
        "been successfully processed."
    )

else:

    new_results = []

    total = len(remaining_df)

    print("\nStarting LLM processing...")
    print("-" * 60)

    for position, (_, row) in enumerate(
        remaining_df.iterrows(),
        start=1
    ):

        report_id = str(row["report_id"])

        report_text = str(
            row["crimeaditionalinfo"]
        )

        print(
            f"\nProcessing report "
            f"{position}/{total}"
        )

        result = analyze_report(
            report_id,
            report_text
        )

        # Preserve original dataset fields
        result["category"] = row["category"]
        result["sub_category"] = row["sub_category"]

        new_results.append(result)

        if result["processing_status"] == "success":

            print("✓ Successfully analyzed")

        else:

            print("✗ Processing failed")

            print(
                f"  Error: {result['error']}"
            )

        # Save after every report
        existing_results = save_checkpoint(
            existing_results,
            new_results
        )

        print("  Checkpoint saved.")

        # Wait before next API request
        time.sleep(SLEEP_SECONDS)


# ============================================================
# FINAL SUMMARY
# ============================================================

if os.path.exists(OUTPUT_FILE):

    final_results = pd.read_csv(
        OUTPUT_FILE
    )

    # Final duplicate protection
    final_results = final_results.drop_duplicates(
        subset=["report_id"],
        keep="last"
    )

    final_results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("             BATCH PROCESSING SUMMARY")
    print("=" * 60)

    print(
        f"\nTotal checkpoint records: "
        f"{len(final_results)}"
    )

    if "processing_status" in final_results.columns:

        print("\nProcessing status:")

        print(
            final_results[
                "processing_status"
            ].value_counts()
        )

    print("\nOutput saved to:")
    print(OUTPUT_FILE)


print("\n" + "=" * 60)
print("                 PIPELINE COMPLETE")
print("=" * 60)