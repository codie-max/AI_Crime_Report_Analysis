import pandas as pd

# File paths
INPUT_PATH = "data/raw/train.csv"
OUTPUT_PATH = "data/processed/cleaned_crime_reports.csv"


def load_data():
    """Load the raw crime report dataset."""
    return pd.read_csv(INPUT_PATH)


def clean_data(df):
    """Clean and prepare crime report data."""

    # Remove rows where crime report text is missing
    df = df.dropna(subset=["crimeaditionalinfo"]).copy()

    # Fill missing subcategories
    df["sub_category"] = df["sub_category"].fillna("Unknown")

    # Clean whitespace from text fields
    df["category"] = df["category"].str.strip()
    df["sub_category"] = df["sub_category"].str.strip()
    df["crimeaditionalinfo"] = (
        df["crimeaditionalinfo"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove empty report text
    df = df[df["crimeaditionalinfo"] != ""]

    # Remove duplicates AFTER cleaning
    df = df.drop_duplicates().copy()

    return df

def main():
    print("=" * 60)
    print("       CRIME REPORT DATA PREPROCESSING")
    print("=" * 60)

    # Load data
    df = load_data()

    print(f"\nOriginal records: {len(df)}")

    # Clean data
    cleaned_df = clean_data(df)

    print(f"Cleaned records: {len(cleaned_df)}")
    print(f"Records removed: {len(df) - len(cleaned_df)}")

    # Save cleaned dataset
    cleaned_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCleaned dataset saved to:")
    print(OUTPUT_PATH)

    print("\nFinal dataset shape:")
    print(cleaned_df.shape)

    print("\nRemaining missing values:")
    print(cleaned_df.isnull().sum())

    print("\n" + "=" * 60)
    print("          PREPROCESSING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()