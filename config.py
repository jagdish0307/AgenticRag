import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face API Key (Loaded from .env)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")



# API URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CLINICALTRIALS_API_URL = "https://clinicaltrials.gov/api/query"

# LLM Models (Hugging Face)
LLM_MODELS = {
    "text_understanding": "mistralai/Mistral-7B",
    "data_extraction": "bigscience/T0pp",
    "answer_generation": "tiiuae/falcon-7b-instruct"
}
