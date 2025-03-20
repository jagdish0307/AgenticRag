import faiss
import pickle
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_faiss_index(index_path="embeddings/faiss_index"):
    """Load FAISS index and metadata."""
    try:
        # Load FAISS index
        index = faiss.read_index(f"{index_path}.index")
        
        # Load metadata
        with open(f"{index_path}.pkl", "rb") as f:
            documents = pickle.load(f)
        
        print("✅ FAISS Index Loaded Successfully!")
        return index, documents
    except Exception as e:
        print(f"❌ Error loading FAISS index: {e}")
        return None, None

def search_faiss(query, top_k=3):
    """Search FAISS index for similar documents."""
    index, documents = load_faiss_index()
    if index is None or documents is None:
        return None
    
    # Load embeddings model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = np.array([embedding_model.embed_query(query)]).astype("float32")
    
    # Perform search
    distances, indices = index.search(query_embedding, top_k)
    
    # Return results
    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])
    
    if results:
        print("✅ Relevant data found in FAISS! Stopping further search.")
    return results if results else None

if __name__ == "__main__":
    query = "tell me how many District hospital?"
    result = search_faiss(query)
    print("FAISS Search Result:", result)
