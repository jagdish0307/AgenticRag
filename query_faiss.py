import faiss
import pickle
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ Load FAISS index
def load_faiss_index(index_name="faiss_index"):
    index = faiss.read_index(f"{index_name}.index")
    with open(f"{index_name}.pkl", "rb") as f:
        text_chunks = pickle.load(f)
    return index, text_chunks

# ✅ Search FAISS
def search_faiss(query, top_k=3, index_name="faiss_index"):
    index, text_chunks = load_faiss_index(index_name)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Convert query into embedding
    query_embedding = np.array([embedding_model.embed_query(query)]).astype("float32")

    # Perform FAISS search
    distances, indices = index.search(query_embedding, top_k)

    # Get matching text chunks
    results = [text_chunks[i] for i in indices[0]]
    return results

if __name__ == "__main__":
    user_query = input("🔍 Enter your query: ")
    matches = search_faiss(user_query)

    print("\n✅ Top Matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n🔹 Match {i}: {match}")
