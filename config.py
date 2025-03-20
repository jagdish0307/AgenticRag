import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Hugging Face API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Hugging Face Model Name
HUGGINGFACE_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# API URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CLINICALTRIALS_API_URL = "https://clinicaltrials.gov/api/query"

# LLM Models (Hugging Face)
LLM_MODELS = {
    "text_understanding": "mistralai/Mistral-7B",
    "data_extraction": "bigscience/T0pp",
    "answer_generation": "tiiuae/falcon-7b-instruct"
}
