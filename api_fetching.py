import requests
import json
import os

# ✅ ClinicalTrials API
def fetch_clinical_trials_data(query="diabetes"):
    """Fetch clinical trials data from ClinicalTrials.gov API."""
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={query}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors

        data = response.json()
        if data:
            print("✅ ClinicalTrials Data Fetched Successfully!")
            return data
        else:
            print("⚠️ No data found for query:", query)
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ClinicalTrials API Error: {e}")
        return None

# ✅ PubMed API
def fetch_pubmed_data(query="cancer treatment"):
    """Fetch medical research data from PubMed API."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if data:
            print("✅ PubMed Data Fetched Successfully!")
            return data
        else:
            print("⚠️ No data found for query:", query)
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ PubMed API Error: {e}")
        return None

# ✅ Store API Data in JSON
def save_data_to_json(data, filename):
    """Save API response data to a JSON file."""
    if data:
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data saved to {filename}")
    else:
        print(f"⚠️ No data to save for {filename}")

# ✅ Run APIs
if __name__ == "__main__":
    clinical_trials_data = fetch_clinical_trials_data()
    pubmed_data = fetch_pubmed_data()

    save_data_to_json(clinical_trials_data, "data/clinical_trials_data.json")
    save_data_to_json(pubmed_data, "data/pubmed_data.json")
