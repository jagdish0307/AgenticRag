import sys
import os

# ✅ Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval_tools.pdf_tool import search_pdf

query = "What are the limitations of current ethical guidelines for public health research?"

response = search_pdf(query)
print("\n📄 PDF Search Result:\n")
print(response)
