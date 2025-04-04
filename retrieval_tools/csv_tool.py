import os
import sys
import pandas as pd
import json
import re
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Ensure we can import config.py from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config  # ✅ Importing paths from config

# Load environment variables
load_dotenv()

# ✅ Use paths from config
CSV_FILE_PATH = config.CSV_FILE_PATH
DB_PATH = config.DB_PATH

# Ensure the `data/` directory exists
os.makedirs("data", exist_ok=True)

COLUMNS_TO_KEEP = [
    "name", "age", "gender", "blood_type", "medical_condition", "date_of_admission",
    "doctor", "hospital", "insurance_provider", "billing_amount", "room_number",
    "admission_type", "discharge_date", "medication", "test_results"
]

class HealthcareCSVHandler:
    def __init__(self):
        """Initialize database connection and load CSV data."""
        self.db_engine = create_engine(f"sqlite:///{DB_PATH}")  # ✅ From config
        self.load_csv_to_db()

    def load_csv_to_db(self):
        """Loads CSV data into an SQLite database."""
        if not os.path.exists(CSV_FILE_PATH):
            print(f"❌ CSV file not found: {CSV_FILE_PATH}")
            return

        df = pd.read_csv(CSV_FILE_PATH).fillna("")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Store in SQLite database
        df.to_sql("healthcare_data", self.db_engine, index=False, if_exists="replace")
        print("✅ CSV data loaded into SQL database.")

    def extract_name_from_query(self, query):
        """
        Extracts a patient name from the query.
        - Handles case variations (e.g., 'bObBy jAcksoN' → 'Bobby Jackson')
        - Removes extra words like "Find", "Details", "for"
        """
        query = query.lower()
        query = re.sub(r'\b(find|details|for|about|patient)\b', '', query)
        words = query.strip().split()

        if len(words) >= 2:
            return " ".join(words[:2]).title()
        return None

    def query_csv(self, query):
        """Queries patient records from the database."""
        try:
            patient_name = self.extract_name_from_query(query)
            if not patient_name:
                return {"error": "Could not extract patient name from query."}

            query_str = f"SELECT * FROM healthcare_data WHERE LOWER(name) LIKE LOWER(:name) LIMIT 50"
            df = pd.read_sql(query_str, self.db_engine, params={"name": f"%{patient_name}%"})

            if df.empty:
                return {"error": f"No records found for '{patient_name}'."}

            relevant_columns = [col for col in COLUMNS_TO_KEEP if col in df.columns]
            return json.loads(df[relevant_columns].to_json(orient="records"))
        except Exception as e:
            return {"error": f"CSV Query Error: {e}"}


if __name__ == "__main__":
    handler = HealthcareCSVHandler()
    test_queries = [
        "Find details for Bobby JacksOn",
        "Find details about danny smith",
        "Patient information for CHRISTINA MARTINEZ",
        "Find patient details for Brooke Brady"
    ]

    for query in test_queries:
        print(f"🔍 Query: {query}")
        print(handler.query_csv(query))
        print("=" * 50)
