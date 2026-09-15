import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# ============================================================
# AI-BASED CRIME OBSERVATIONS
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)

INPUT_FILE = "data/processed/llm_structured_crime_records.csv"
OUTPUT_FILE = "data/processed/crime_records_with_observations.csv"

# ------------------------------------------------------------
# Load structured crime records
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("        AI-BASED CRIME OBSERVATIONS")
print("=" * 60)

print(f"\nTotal structured records: {len(df)}")

observations = []

# ------------------------------------------------------------
# Generate observations
# ------------------------------------------------------------

for i, row in df.iterrows():

    print(f"\nAnalyzing observation {i + 1}/{len(df)}...")

    prompt = f"""
You are an AI crime analysis assistant.

Analyze the following structured cybercrime record and provide
one concise AI-based observation.

Crime Type:
{row.get("crime_type", "Not specified")}

Summary:
{row.get("summary", "Not specified")}

Modus Operandi:
{row.get("modus_operandi", "Not specified")}

Platforms:
{row.get("platforms", "Not specified")}

Location:
{row.get("location", "Not specified")}

Financial Loss:
{row.get("financial_loss", "Not specified")}

Severity:
{row.get("severity", "Not specified")}

Provide an observation that identifies the important pattern,
risk, or behavior visible in this report.

Do not invent facts that are not present in the report.

Return only the observation in 2-3 sentences.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        observation = response.text.strip()

        observations.append(observation)

        print("✓ Observation generated")

    except Exception as e:

        print(f"✗ Error: {e}")

        observations.append("Observation could not be generated.")

# ------------------------------------------------------------
# Add observations to dataframe
# ------------------------------------------------------------

df["ai_observation"] = observations

# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("             AI OBSERVATIONS COMPLETE")
print("=" * 60)

print("\nSample AI Observations:")
print("-" * 60)

for i in range(min(5, len(df))):

    print(f"\nReport {i + 1}:")
    print(df.loc[i, "ai_observation"])

print("\n" + "=" * 60)
print("Results saved to:")
print(OUTPUT_FILE)
print("=" * 60)