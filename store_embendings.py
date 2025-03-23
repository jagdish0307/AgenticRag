import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_text(file_path):
    """Load text from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_embeddings(docs, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Generate embeddings for the provided documents."""
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings, embeddings.embed_documents(docs)

def store_embeddings(docs, embeddings, faiss_index_path="faiss_index"):
    """Store embeddings in a FAISS index."""
    if os.path.exists(faiss_index_path):
        print(f"🔄 Loading existing FAISS index from {faiss_index_path}...")
        faiss_index = FAISS.load_local(faiss_index_path, embeddings)
    else:
        print("🆕 Creating a new FAISS index...")
        faiss_index = FAISS.from_texts(docs, embeddings)
    faiss_index.save_local(faiss_index_path)
    print(f"✅ Embeddings stored in FAISS index at {faiss_index_path}")

def main():
    text_file_path = os.path.join("data", "extracted_text.txt")
    faiss_index_path = os.path.join("data", "faiss_index")

    print("📄 Loading extracted text...")
    text = load_text(text_file_path)

    print("🔍 Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_text(text)

    print("⚙️ Generating embeddings...")
    embeddings, _ = generate_embeddings(docs)

    print("💾 Storing embeddings in FAISS index...")
    store_embeddings(docs, embeddings, faiss_index_path)

if __name__ == "__main__":
    main()
