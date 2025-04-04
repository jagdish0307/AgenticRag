import sys
import os

# ✅ Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval_tools.serpapi_tool import search_health_info

query = "Latest treatments for diabetes in 2024"

response = search_health_info(query)

print("\n🌐 SerpAPI Search Result:\n")
print(response)

