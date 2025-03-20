from api_fetching import fetch_clinical_trials_data, fetch_pubmed_data

def query_apis(query):
    """Query external APIs for additional information if FAISS & CSV fail."""
    clinical_trials = fetch_clinical_trials_data(query)
    pubmed_results = fetch_pubmed_data(query)

    if clinical_trials or pubmed_results:
        return {
            "source": "APIs",
            "clinical_trials": clinical_trials if clinical_trials else "No data found",
            "pubmed": pubmed_results if pubmed_results else "No data found"
        }

    return None
