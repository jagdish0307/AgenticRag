import os
import pandas as pd
import json

CSV_FILE_PATH = "data/healthcare_dataset.csv"

def query_csv(query):
    """Query patient records from CSV."""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return {"error": "CSV file not found."}

        df = pd.read_csv(CSV_FILE_PATH)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        if "name" not in df.columns:
            return {"error": "CSV does not contain 'Name' column."}

        # Extract patient name from query
        words = query.lower().split()
        patient_name = " ".join(words[-2:])  # ✅ Extracts last two words safely

        # Perform case-insensitive matching
        filtered_df = df[df["name"].str.lower() == patient_name]
        if filtered_df.empty:
            filtered_df = df[df["name"].str.contains(patient_name.split()[0], case=False, na=False)]

        if filtered_df.empty:
            return {"error": f"No records found for {patient_name}."}

        # Selecting only relevant columns
        relevant_columns = [col for col in ["name", "blood_type", "medical_condition", "doctor", "hospital"] if col in df.columns]
        return json.loads(filtered_df[relevant_columns].to_json(orient="records"))

    except Exception as e:
        return {"error": f"CSV Query Error: {e}"}
