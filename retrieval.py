
import json
from retrieval_tools.csv_tool import query_csv
from retrieval_tools.faiss_tool import search_faiss
from retrieval_tools.api_tool import query_apis

def retrieve_data(query):
    """Retrieve data from CSV, FAISS, or APIs based on availability."""
    print(f"🔍 Searching for: {query}")

    # 1️⃣ Query CSV
    try:
        csv_results = query_csv(query)
        if csv_results and isinstance(csv_results, (list, dict)) and "error" not in str(csv_results).lower():
            print("✅ Data found in CSV.")
            return {
                "source": "CSV",
                "confidence": 0.9,
                "data": csv_results,
                "source_info": "healthcare_dataset.csv"
            }
        else:
            print("❌ No relevant data found in CSV. Trying FAISS...")
    except FileNotFoundError:
        print("⚠️ CSV file not found. Trying FAISS...")
    except Exception as e:
        print(f"⚠️ CSV query failed: {e}")

    # 2️⃣ Query FAISS
    try:
        faiss_results = search_faiss(query)
        if isinstance(faiss_results, tuple) and len(faiss_results) == 2:
            faiss_data, faiss_score = faiss_results
            if faiss_data:
                print("✅ Data found in FAISS.")
                return {
                    "source": "FAISS",
                    "confidence": faiss_score,
                    "data": faiss_data,
                    "source_info": "faiss_index"
                }
        print("❌ No relevant data found in FAISS. Trying API...")
    except Exception as e:
        print(f"⚠️ FAISS query failed: {e}")

    # 3️⃣ Query APIs
    try:
        api_results = query_apis(query)
        if api_results and isinstance(api_results, (list, dict)) and "error" not in str(api_results).lower():
            print("✅ Data found in APIs.")
            return {
                "source": "API",
                "confidence": 0.8,
                "data": api_results,
                "source_info": "PubMed API / ClinicalTrials API"
            }
        else:
            print("❌ No relevant data found in API sources.")
    except ConnectionError:
        print("⚠️ API connection failed.")
    except Exception as e:
        print(f"⚠️ API query failed: {e}")

    print("❌ No relevant information found in any source.")
    return {
        "source": "None",
        "confidence": 0.0,
        "data": "No relevant information found."
    }

# Example Query
if __name__ == "__main__":
    user_query = "What are the latest clinical trials for Parkinson’s disease?"
    response = retrieve_data(user_query)
    print(json.dumps(response, indent=2))
