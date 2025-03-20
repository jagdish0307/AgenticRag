import requests
import json

# ✅ ClinicalTrials API
def fetch_clinical_trials_data(query="diabetes"):
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={query}&format=json"
    try:
        response = requests.get(url)
        print(f"ClinicalTrials API Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ ClinicalTrials Data Fetched Successfully!")
            return data
        else:
            print("❌ ClinicalTrials API Request Failed!")
            return None
    except Exception as e:
        print(f"❌ ClinicalTrials API Error: {e}")
        return None

# ✅ PubMed API
def fetch_pubmed_data(query="cancer treatment"):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json"
    try:
        response = requests.get(url)
        print(f"PubMed API Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ PubMed Data Fetched Successfully!")
            return data
        else:
            print("❌ PubMed API Request Failed!")
            return None
    except Exception as e:
        print(f"❌ PubMed API Error: {e}")
        return None

# ✅ Store API Data in JSON
def save_data_to_json(data, filename):
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data saved to {filename}")

# ✅ Run APIs
if __name__ == "__main__":
    clinical_trials_data = fetch_clinical_trials_data()
    pubmed_data = fetch_pubmed_data()

    save_data_to_json(clinical_trials_data, "data/clinical_trials_data.json")
    save_data_to_json(pubmed_data, "data/pubmed_data.json")
