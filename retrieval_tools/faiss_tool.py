import os
import faiss
import pickle
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings  # ✅ Corrected import

# ✅ Load Hugging Face embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ FAISS paths
FAISS_INDEX_PATH = "embeddings/faiss_index.index"
FAISS_MAPPING_PATH = "embeddings/faiss_index.pkl"

def load_faiss_index():
    """Load FAISS index and document mappings."""
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(FAISS_MAPPING_PATH):
        raise FileNotFoundError("❌ FAISS index or mapping file not found.")

    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_MAPPING_PATH, "rb") as f:
            documents = pickle.load(f)
        return index, documents
    except Exception as e:
        raise RuntimeError(f"❌ Error loading FAISS: {e}")

def search_faiss(query, top_k=5, threshold=0.75):
    """Search FAISS index for relevant embeddings."""
    try:
        index, documents = load_faiss_index()
        query_embedding = np.array([embedding_model.embed_query(query)]).astype("float32")
        D, I = index.search(query_embedding, top_k)

        # Convert FAISS distances to similarity scores
        similarities = 1 - D[0]
        results = [
            (documents[i], similarities[idx])
            for idx, (i, score) in enumerate(zip(I[0], similarities))
            if i != -1 and score >= threshold and i in documents  # ✅ Prevents missing index errors
        ]
        return results if results else []
    except Exception as e:
        raise RuntimeError(f"❌ FAISS Search Error: {e}")
