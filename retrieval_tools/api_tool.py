import requests
import os

# Load API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "tiiuae/falcon-7b-instruct"

def query_huggingface_api(prompt):
    """Query Hugging Face API for LLM inference."""
    if not HUGGINGFACE_API_KEY:
        return {"error": "Hugging Face API key is missing."}

    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 50}}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)  # ✅ Added timeout
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            return {"response": data[0].get("generated_text", "No response")}
        return {"error": "Unexpected API response format."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Exception: {e}"}

# ✅ ClinicalTrials API Integration
def query_clinical_trials(query):
    """Fetch clinical trials data from ClinicalTrials.gov API."""
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={query}&format=json"
    try:
        response = requests.get(url, timeout=10)  # ✅ Added timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"ClinicalTrials API Error: {e}"}

# ✅ PubMed API Integration
def query_pubmed(query):
    """Fetch medical research data from PubMed API."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json"
    try:
        response = requests.get(url, timeout=10)  # ✅ Added timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"PubMed API Error: {e}"}
