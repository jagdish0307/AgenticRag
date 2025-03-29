import os
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from .env
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("⚠️ SERPAPI_API_KEY is missing! Add it to your .env file.")

# Initialize SerpAPI Wrapper
serp = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

def search_health_info(query):
    """Search health-related queries using SerpAPI."""
    try:
        results = serp.run(query)
        return results
    except Exception as e:
        return {"error": f"SerpAPI search failed: {str(e)}"}
