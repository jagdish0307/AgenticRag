import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)

if response.status_code == 200:
    print("✅ API Key is valid! User Info:", response.json())
else:
    print(f"❌ API Key Error! Status Code: {response.status_code}, Response: {response.text}")
