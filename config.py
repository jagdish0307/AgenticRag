# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()



# # OpenAI API Key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Hugging Face API Key
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# # Hugging Face Model Name
# HUGGINGFACE_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# # SerpAPI Key
# SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# # GroqAPI Key
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # API URLs
# PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# CLINICALTRIALS_API_URL = "https://clinicaltrials.gov/api/query"

# # LLM Models (Hugging Face)
# LLM_MODELS = {
#     "text_understanding": "mistralai/Mistral-7B",
#     "data_extraction": "bigscience/T0pp",
#     "answer_generation": "tiiuae/falcon-7b-instruct"
# }


# config.py

import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ✅ API Base URL for Groq
GROQ_API_BASE = "https://api.groq.com/openai/v1"


# ✅ Model Names
HUGGINGFACE_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GEMMA_MODEL_NAME = "gemma2-9b-it"

# ✅ API URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CLINICALTRIALS_API_URL = "https://clinicaltrials.gov/api/query"

# ✅ LLM Models for Task-Specific Use
LLM_MODELS = {
    "text_understanding": "mistralai/Mistral-7B",
    "data_extraction": "bigscience/T0pp",
    "answer_generation": "tiiuae/falcon-7b-instruct",
    "refinement": GEMMA_MODEL_NAME  # For user-friendly refinement
}


# ✅ File Paths
CSV_FILE_PATH = "data/healthcare_dataset.csv"
DB_PATH = "data/healthcare_data.db"
PDF_FILE_PATH = "data/Public_Health_Research.pdf"
FAISS_PATH = "embedding"

# Path to default PDF for testing
DEFAULT_PDF_PATH = "data/Public_Health_Research.pdf"


# Embedding model used across tools
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
