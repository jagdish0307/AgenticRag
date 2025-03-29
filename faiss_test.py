from retrieval_tools.pdf_tool import search_pdf

query = " What are the limitations of current ethical guidelines for public health research?"

response = search_pdf(query)
print(response)
