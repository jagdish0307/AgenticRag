import os
import pickle
import faiss
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

# Define FAISS index paths
FAISS_INDEX_PATH = "embeddings/faiss_index.index"
FAISS_MAPPING_PATH = "embeddings/faiss_index.pkl"

# Initialize embedding model (updated import & model selection for free-tier Hugging Face)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_faiss_index():
    """Loads the FAISS index and mapping if available."""
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_MAPPING_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_MAPPING_PATH, "rb") as f:
            mapping = pickle.load(f)
        return FAISS(index, embedding_model), mapping
    return None, {}

def save_faiss_index(faiss_store, mapping):
    """Saves the FAISS index and mapping."""
    faiss.write_index(faiss_store.index, FAISS_INDEX_PATH)
    with open(FAISS_MAPPING_PATH, "wb") as f:
        pickle.dump(mapping, f)

def store_documents(documents):
    """Stores documents in FAISS after embedding them."""
    faiss_store = FAISS.from_documents(documents, embedding_model)
    mapping = {i: doc.metadata for i, doc in enumerate(documents)}
    save_faiss_index(faiss_store, mapping)

def search_faiss(query, top_k=5):
    """Performs a hybrid search (vector + keyword)."""
    faiss_store, mapping = load_faiss_index()
    if not faiss_store:
        return "No FAISS index found. Please store documents first."
    
    # Perform vector search
    docs_and_scores = faiss_store.similarity_search_with_score(query, k=top_k)
    
    # Format results
    results = [
        {
            "content": doc.page_content,
            "metadata": mapping.get(i, {})
        }
        for i, (doc, score) in enumerate(docs_and_scores)
    ]
    return results
