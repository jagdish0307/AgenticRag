import sys
import os

# ✅ Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval_tools.csv_tool import HealthcareCSVHandler

handler = HealthcareCSVHandler()

test_queries = [
    "Find details for Bobby JacksOn",
    "Find patient details for Brooke Brady"
]

for query in test_queries:
    print(f"\n🔍 Query: {query}")
    result = handler.query_csv(query)
    print(result)
    print("=" * 50)
