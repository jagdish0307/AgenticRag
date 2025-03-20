import os
import pandas as pd
import json
import requests

# Load API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "tiiuae/falcon-7b-instruct"  # Free Model
CSV_FILE_PATH = "data/healthcare_dataset.csv"

def query_csv(query):
    """Query patient records from CSV using Hugging Face API for better understanding."""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return {"error": "CSV file not found."}
        
        df = pd.read_csv(CSV_FILE_PATH)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        if "name" not in df.columns:
            return {"error": "CSV does not contain 'Name' column."}

        # Extract patient name from query
        words = query.lower().split()
        patient_name = " ".join(words[-2:])

        # Filter for exact match or partial match
        filtered_df = df[df["name"].str.lower() == patient_name]
        if filtered_df.empty:
            filtered_df = df[df["name"].str.contains(patient_name.split()[0], case=False, na=False)]

        if filtered_df.empty:
            return {"error": f"No records found for {patient_name}."}

        relevant_columns = ["name", "blood_type", "medical_condition", "doctor", "hospital"]
        filtered_df = filtered_df[relevant_columns]
        data_json = filtered_df.to_json(orient="records", indent=2)

        # Truncate if needed
        if len(data_json) > 1000:
            data_json = json.dumps(filtered_df.iloc[0].to_dict(), indent=2)

        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": f"Extract blood type from this record:\n{data_json}\nQuery: {query}",
            "parameters": {"max_new_tokens": 30}
        }

        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        return {"error": response.text}
    except Exception as e:
        return {"error": f"CSV Query Error: {e}"}
