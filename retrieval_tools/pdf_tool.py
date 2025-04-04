
import os
import fitz  # PyMuPDF for PDF parsing
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config  # ✅ Import FAISS path and embeddings model name

# ✅ Load config-based embedding model and FAISS storage path
FAISS_PATH = config.FAISS_PATH
EMBEDDING_MODEL_NAME = config.EMBEDDING_MODEL_NAME
os.makedirs(FAISS_PATH, exist_ok=True)

# ✅ Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

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

    # ✅ Convert to LangChain Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"✅ Extracted {len(documents)} chunks from PDF.")

    # ✅ Store to FAISS
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
    vectorstore = load_faiss()
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([f"📄 **Match {i+1}:**\n{doc.page_content}" for i, doc in enumerate(results)])

if __name__ == "__main__":
    # ✅ Example usage
    pdf_path = config.DEFAULT_PDF_PATH  # Config-managed test PDF path
    process_pdf(pdf_path)

    query = "What are the  Protection of Vulnerable Populations ?"
    print(search_pdf(query))
