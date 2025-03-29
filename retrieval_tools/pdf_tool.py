import os
import fitz  # PyMuPDF for PDF parsing
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# # ✅ Define FAISS storage path
FAISS_PATH = "embedding"
os.makedirs(FAISS_PATH, exist_ok=True)

# ✅ Load Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_pdf(fpath, max_pages=20):
    """Load text from a PDF file."""
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"❌ PDF file not found: {fpath}")

    doc = fitz.open(fpath)
    text = "\n\n".join(
        doc[i].get_text("text") for i in range(min(max_pages, len(doc))) if doc[i].get_text("text").strip()
    )
    
    return text

def process_pdf(pdf_path, chunk_size=500, chunk_overlap=100):
    """Extract text from PDF, split into chunks, and store in FAISS."""
    print(f"📄 Processing PDF: {pdf_path}")

    # ✅ Extract text
    raw_text = load_pdf(pdf_path)
    if not raw_text:
        raise ValueError("❌ No text found in the PDF!")

    # ✅ Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(raw_text)
    
    # ✅ Convert chunks into LangChain Document format
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    print(f"✅ Extracted {len(documents)} chunks from PDF.")

    # ✅ Create FAISS index
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_PATH)
    
    print(f"🎯 FAISS index created and saved at: {FAISS_PATH}")

def load_faiss():
    """Load the FAISS index and return the vectorstore."""
    if not os.path.exists(FAISS_PATH):
        raise FileNotFoundError("❌ FAISS index not found! Run `process_pdf()` first.")

    vectorstore = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS index loaded successfully!")
    return vectorstore

def search_pdf(query, k=3):
    """Retrieve relevant information from FAISS-indexed healthcare PDFs."""
    vectorstore = load_faiss()  # ✅ Load FAISS index
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([f"📄 **Match {i+1}:**\n{doc.page_content}" for i, doc in enumerate(results)])

if __name__ == "__main__":
    # ✅ Example usage
    pdf_path = "data/Public_Health_Research.pdf"  # Change to your actual PDF path
    process_pdf(pdf_path)

    # ✅ Test search
    query = "What are the key findings in public health research?"
    print(search_pdf(query))
