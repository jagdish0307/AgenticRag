import os
import pickle
import faiss
import numpy as np
from retrieval_tools.api_tool import query_clinical_trials, query_pubmed, query_huggingface_api
from retrieval_tools.csv_tool import query_csv
from retrieval_tools.faiss_tool import search_faiss, load_faiss_index

# ✅ FAISS Index Paths
FAISS_INDEX_PATH = "embeddings/faiss_index.index"
FAISS_MAPPING_PATH = "embeddings/faiss_index.pkl"

# ✅ Load FAISS index and mapping
def load_faiss():
    """Load FAISS index and document mapping."""
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(FAISS_MAPPING_PATH):
        raise FileNotFoundError("❌ FAISS index or mapping file is missing.")

    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(FAISS_MAPPING_PATH, "rb") as f:
        mapping = pickle.load(f)

    return index, mapping

# ✅ FAISS-based retrieval
def retrieve_faiss(query, top_k=3):
    """Retrieve relevant data from FAISS using embeddings."""
    return search_faiss(query, top_k=top_k)

# ✅ Retrieve clinical trials data
def retrieve_clinical_trials(query):
    """Fetch related clinical trial studies."""
    return query_clinical_trials(query)

# ✅ Retrieve PubMed research data
def retrieve_pubmed(query):
    """Fetch PubMed articles relevant to query."""
    return query_pubmed(query)

# ✅ Retrieve patient records from CSV
def retrieve_patient_data(query):
    """Fetch patient record from CSV file."""
    return query_csv(query)

# ✅ Hugging Face LLM Integration
def generate_response_with_huggingface(prompt):
    """Query Hugging Face LLM model for additional insights."""
    return query_huggingface_api(prompt)

# ✅ Unified retrieval function
def retrieve_info(query, patient_query=None, use_llm=False):
    """
    Retrieve relevant data from FAISS, ClinicalTrials, PubMed, CSV, and optionally LLM.
    
    Args:
    - query (str): The main query string.
    - patient_query (str, optional): The patient name for CSV retrieval.
    - use_llm (bool, optional): Whether to use LLM for additional insights.
    
    Returns:
    - dict: Combined results from all sources.
    """
    faiss_results = retrieve_faiss(query)
    clinical_trials = retrieve_clinical_trials(query)
    pubmed_results = retrieve_pubmed(query)
    patient_data = retrieve_patient_data(patient_query) if patient_query else "No patient query provided."
    llm_response = generate_response_with_huggingface(query) if use_llm else "LLM response disabled."

    return {
        "FAISS Results": faiss_results,
        "Clinical Trials": clinical_trials,
        "PubMed Articles": pubmed_results,
        "Patient Data": patient_data,
        "LLM Response": llm_response,
    }

# ✅ Test the retrieval pipeline
if __name__ == "__main__":
    test_query = "Latest treatment for diabetes"
    test_patient_query = "John Doe"
    
    results = retrieve_info(test_query, test_patient_query, use_llm=True)
    for key, value in results.items():
        print(f"\n{key}: {value}")
