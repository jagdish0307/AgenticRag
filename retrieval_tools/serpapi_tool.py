
import sys
import os
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv

# ✅ Enable parent folder import for config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config  # ✅ Import SERPAPI_API_KEY

# ✅ Load environment variables
load_dotenv()

# ✅ Get SerpAPI key from config
SERPAPI_API_KEY = config.SERPAPI_API_KEY

if not SERPAPI_API_KEY:
    raise ValueError("⚠️ SERPAPI_API_KEY is missing! Add it to your .env file or config.py.")

# ✅ Initialize SerpAPI wrapper
serp = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

def search_health_info(query):
    """Search health-related queries using SerpAPI."""
    try:
        results = serp.run(query)
        return results
    except Exception as e:
        return {"error": f"SerpAPI search failed: {str(e)}"}

if __name__ == "__main__":
    test_query = "Latest treatments for diabetes in 2024"
    print("🔍 SerpAPI Test Query:", test_query)
    print(search_health_info(test_query))
