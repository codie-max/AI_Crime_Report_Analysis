import pandas as pd
import re


DATA_PATH = "data/processed/cleaned_crime_reports.csv"


# --------------------------------------------------
# Text Cleaning Function
# --------------------------------------------------

def clean_text(text):
    """
    Perform basic NLP text cleaning.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Crime-related Keyword Dictionary
# --------------------------------------------------

CRIME_KEYWORDS = {
    "financial": [
        "money",
        "fraud",
        "payment",
        "transaction",
        "bank",
        "upi",
        "loan",
        "credit",
        "debit",
        "refund"
    ],

    "social_media": [
        "whatsapp",
        "facebook",
        "instagram",
        "telegram",
        "social media",
        "profile"
    ],

    "cyber_attack": [
        "hacking",
        "hacked",
        "malware",
        "ransomware",
        "virus",
        "password",
        "account"
    ],

    "harassment": [
        "threat",
        "threatening",
        "abusive",
        "harassment",
        "stalking",
        "blackmail",
        "nude"
    ],

    "job_fraud": [
        "job",
        "interview",
        "work from home",
        "security amount",
        "insurance"
    ]
}


# --------------------------------------------------
# Keyword Extraction Function
# --------------------------------------------------

def extract_keywords(text):
    """
    Identify crime-related keywords present in a report.
    """

    detected_keywords = {}

    for category, keywords in CRIME_KEYWORDS.items():

        found = []

        for keyword in keywords:
            if keyword in text:
                found.append(keyword)

        if found:
            detected_keywords[category] = found

    return detected_keywords


# --------------------------------------------------
# Load Cleaned Dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("             NLP ANALYSIS")
print("=" * 60)

print(f"\nTotal reports: {len(df)}")


# --------------------------------------------------
# Apply Text Cleaning
# --------------------------------------------------

df["cleaned_text"] = df["crimeaditionalinfo"].apply(clean_text)


# --------------------------------------------------
# Apply Keyword Extraction
# --------------------------------------------------

df["detected_keywords"] = df["cleaned_text"].apply(extract_keywords)


# --------------------------------------------------
# Display Results
# --------------------------------------------------

print("\nKeyword Extraction Results")
print("-" * 60)

for i in range(5):

    print(f"\nReport {i + 1}")

    print("Crime Category:")
    print(df.loc[i, "category"])

    print("\nDetected Keywords:")
    print(df.loc[i, "detected_keywords"])

    print("\nReport:")
    print(df.loc[i, "crimeaditionalinfo"])


print("\n" + "=" * 60)
print("        KEYWORD EXTRACTION COMPLETE")
print("=" * 60)