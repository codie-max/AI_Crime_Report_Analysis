import os
import json

from dotenv import load_dotenv
from google import genai

from src.prompts import CRIME_ANALYSIS_PROMPT


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# JSON CLEANING
# ============================================================

def clean_json_response(response_text):

    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    return response_text.strip()


# ============================================================
# SINGLE CRIME REPORT ANALYZER
# ============================================================

def analyze_crime_report(crime_report):

    if not crime_report or not str(crime_report).strip():
        raise ValueError(
            "Crime report cannot be empty."
        )

    prompt = CRIME_ANALYSIS_PROMPT.format(
        crime_report=str(crime_report)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = clean_json_response(
        response.text
    )

    analysis = json.loads(response_text)

    return analysis