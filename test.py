# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# headers = {"Authorization": f"Bearer {API_KEY}"}
# response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)

# if response.status_code == 200:
#     print("✅ API Key is valid! User Info:", response.json())
# else:
#     print(f"❌ API Key Error! Status Code: {response.status_code}, Response: {response.text}")

from langchain_community.tools import PubmedQueryRun

# Create a PubMed tool
pubmed_tool = PubmedQueryRun()

# Example: Fetch latest articles on Parkinson’s disease
query = "Parkinson's disease latest research"
response = pubmed_tool.run(query)

print(response)  # Returns full research articles instead of just IDs
