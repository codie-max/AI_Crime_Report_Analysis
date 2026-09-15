import sqlite3
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "crime_reports.db"

LLM_RESULTS_PATH = (
    BASE_DIR / "data" / "processed" / "llm_batch_results.csv"
)


# ---------------------------------------------------------
# CREATE DATABASE TABLE
# ---------------------------------------------------------

def create_database():

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crime_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER UNIQUE,
            category TEXT,
            sub_category TEXT,
            crime_type TEXT,
            summary TEXT,
            modus_operandi TEXT,
            platforms TEXT,
            entities TEXT,
            location TEXT,
            temporal_information TEXT,
            financial_loss TEXT,
            severity TEXT
        )
    """)

    connection.commit()
    connection.close()


# ---------------------------------------------------------
# INSERT LLM RESULTS
# ---------------------------------------------------------

def insert_llm_results():

    if not LLM_RESULTS_PATH.exists():
        print("LLM results file not found.")
        return

    df = pd.read_csv(LLM_RESULTS_PATH)

    # Use only successfully processed records
    if "processing_status" in df.columns:
        df = df[df["processing_status"] == "success"].copy()

    connection = sqlite3.connect(DATABASE_PATH)

    records_inserted = 0

    for _, row in df.iterrows():

        try:
            connection.execute("""
                INSERT OR IGNORE INTO crime_reports (
                    report_id,
                    category,
                    sub_category,
                    crime_type,
                    summary,
                    modus_operandi,
                    platforms,
                    entities,
                    location,
                    temporal_information,
                    financial_loss,
                    severity
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row["report_id"]),
                row["category"],
                row["sub_category"],
                row["crime_type"],
                row["summary"],
                row["modus_operandi"],
                row["platforms"],
                row["entities"],
                row["location"],
                row["temporal_information"],
                row["financial_loss"],
                row["severity"]
            ))

            if connection.total_changes > records_inserted:
                records_inserted += 1

        except Exception as e:
            print(
                f"Error inserting report "
                f"{row.get('report_id')}: {e}"
            )

    connection.commit()
    connection.close()

    print(f"Records inserted: {records_inserted}")


# ---------------------------------------------------------
# VERIFY DATABASE
# ---------------------------------------------------------

def verify_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # Get total number of records
    cursor.execute(
        "SELECT COUNT(*) FROM crime_reports"
    )

    total_records = cursor.fetchone()[0]

    print(f"Total records in database: {total_records}")

    # Retrieve sample records
    cursor.execute("""
        SELECT
            report_id,
            category,
            sub_category,
            crime_type,
            severity
        FROM crime_reports
        LIMIT 5
    """)

    records = cursor.fetchall()

    print("\nSample records:")
    print("-" * 80)

    for record in records:
        print(
            f"Report ID: {record[0]} | "
            f"Category: {record[1]} | "
            f"Subcategory: {record[2]} | "
            f"LLM Crime Type: {record[3]} | "
            f"Severity: {record[4]}"
        )

    connection.close()

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 8 - DATABASE INTEGRATION")
    print("=" * 60)

    create_database()

    insert_llm_results()

    verify_database()

    print("=" * 60)
    print("Database population complete.")
    print("=" * 60)