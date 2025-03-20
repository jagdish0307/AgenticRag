import os
import faiss
import pickle
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

FAISS_INDEX_PATH = "embeddings/faiss_index.index"
FAISS_MAPPING_PATH = "embeddings/faiss_index.pkl"

def load_faiss_index():
    """Load FAISS index and document mappings."""
    try:
        if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(FAISS_MAPPING_PATH):
            return None, None
        
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_MAPPING_PATH, "rb") as f:
            documents = pickle.load(f)
        
        return index, documents
    except Exception as e:
        return None, None

def search_faiss(query, top_k=5, threshold=0.15):
    """Search FAISS index for relevant embeddings."""
    index, documents = load_faiss_index()
    if index is None or not documents:
        return None, 0.0  

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = np.array([embedding_model.embed_query(query)]).astype("float32")
    D, I = index.search(query_embedding, top_k)

    results = [documents[i] for i, score in zip(I[0], D[0]) if i != -1 and score <= threshold]
    return (results, 0.85) if results else (None, 0.0)
