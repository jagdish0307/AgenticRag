import faiss
import pickle
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

# ✅ Load extracted text
def load_text(filename="data/extracted_text.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# ✅ Split text into chunks
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks

# ✅ Generate embeddings and store in FAISS
def store_embeddings_in_faiss(chunks, index_name="faiss_index"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Convert text chunks into embeddings
    embeddings = np.array([embedding_model.embed_query(chunk) for chunk in chunks]).astype("float32")

    # Create FAISS index
    dimension = embeddings.shape[1]  # Get embedding vector size
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Ensure embeddings folder exists
    os.makedirs("embeddings", exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, f"embeddings/{index_name}.index")

    # Store metadata using pickle
    with open(f"embeddings/{index_name}.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Embeddings stored in FAISS successfully.")

if __name__ == "__main__":
    text = load_text()
    chunks = chunk_text(text)
    store_embeddings_in_faiss(chunks)
