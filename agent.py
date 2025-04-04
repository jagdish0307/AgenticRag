# import os
# from langchain.tools import Tool
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain_community.tools.arxiv.tool import ArxivQueryRun
# from retrieval_tools.csv_tool import HealthcareCSVHandler
# from retrieval_tools.serpapi_tool import search_health_info
# from retrieval_tools.pdf_tool import search_pdf
# from langchain_openai import ChatOpenAI
# from langchain.agents import initialize_agent

# # ✅ Load API Key Securely
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # ✅ Define Tools
# wiki = Tool(
#     name="Wikipedia",
#     func=WikipediaAPIWrapper().run,
#     description="Search Wikipedia for general healthcare topics."
# )

# arxiv = Tool(
#     name="Arxiv",
#     func=ArxivQueryRun().run,
#     description="Fetch academic research papers related to healthcare from Arxiv."
# )

# csv_handler = HealthcareCSVHandler()
# patient_info_tool = Tool(
#     name="Patient Records",
#     func=csv_handler.query_csv,
#     description="Retrieve patient medical history from structured CSV records."
# )

# serpapi_tool = Tool(
#     name="Real-Time Healthcare Search",
#     func=search_health_info,
#     description="Fetch the latest healthcare updates and research from the web."
# )

# pdf_faiss_tool = Tool(
#     name="Healthcare PDF Search",
#     func=search_pdf,
#     description="Retrieve information from FAISS-indexed healthcare research PDFs."
# )

# # ✅ List of Tools
# tools = [wiki, arxiv, patient_info_tool, serpapi_tool, pdf_faiss_tool]

# # ✅ Initialize LLM
# llm = ChatOpenAI(
#     model="gemma2-9b-it",
#     temperature=1,
#     openai_api_key=GROQ_API_KEY,
#     openai_api_base="https://api.groq.com/openai/v1"
# )

# # ✅ Initialize Agent
# # ✅ Create the Agent with error handling
# agent_executor = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True  # ✅ Fix output parsing issues
# )


# print("✅ Healthcare AI Chatbot is ready!")

# # ✅ Optimized Prompt for Structured Healthcare Responses
# def refine_response_with_gemma(text):
#     """Formats healthcare responses clearly and concisely using Groq (Gemma 2B)."""
#     prompt = f"""
#     You are a **highly knowledgeable and professional Healthcare AI Assistant**.
#     Your goal is to provide **clear, structured, and easy-to-read healthcare responses**.

#     ### **Response Guidelines:**
#     - **Keep it concise** (avoid unnecessary details and medical jargon).
#     - **Use bullet points** for clarity and easy reading.
#     - **Cite sources when needed** (e.g., Wikipedia, Arxiv, clinical trials).

#     ### **Response Formats:**
#     **1️⃣ General Health Questions:**
#     ✔ **Condition:** [Short explanation]
#     ✔ **Symptoms:** [Common symptoms]
#     ✔ **Treatment:** [Recommended medical treatments]
#     ✔ **Prevention:** [Preventive measures]
#     📢 *Consult a doctor for diagnosis and treatment.*

#     **2️⃣ Clinical Trial Results:**
#     - **Trial Name:** [Name]
#     - **Purpose:** [What is being tested?]
#     - **Phase:** [1, 2, 3, or 4]
#     - **Eligibility:** [Who can join?]
#     - **Enrollment Status:** [Open or Closed]
#     - **Source:** [Website link]

#     **3️⃣ Research Paper Summary:**
#     - **Title:** [Paper Title]
#     - **Published On:** [Date]
#     - **Authors:** [Main Authors]
#     - **Summary:** [Short, easy-to-understand explanation]
#     - **Source:** [Arxiv / PubMed Link]

#     **4️⃣ Patient Records (CSV Data):**
#     - **Patient Name:** [Name]
#     - **Age:** [Age]
#     - **Diagnosis:** [Condition]
#     - **Last Visit:** [Date]
#     - **Prescribed Medications:** [List of meds]
#     📌 *For detailed history, refer to hospital records.*

#     **5️⃣ PDF FAISS Retrieval (Medical Research PDFs):**
#     - **Key Finding:** [Main insight from the PDF]
#     - **Relevance:** [How it applies to the user's query]
#     - **Source:** [PDF file reference]

#     ### **Now, format the following response properly:**
#     {text}
#     """
    
#     response = llm.invoke(prompt)
#     return response.content



import os
from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from retrieval_tools.csv_tool import HealthcareCSVHandler
from retrieval_tools.serpapi_tool import search_health_info
from retrieval_tools.pdf_tool import search_pdf
import config  # ✅ Centralized Config

# ✅ Load API Key from Config
GROQ_API_KEY = config.GROQ_API_KEY

# ✅ Define Tools
wiki = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Search Wikipedia for general healthcare topics."
)

arxiv = Tool(
    name="Arxiv",
    func=ArxivQueryRun().run,
    description="Fetch academic research papers related to healthcare from Arxiv."
)

csv_handler = HealthcareCSVHandler()
patient_info_tool = Tool(
    name="Patient Records",
    func=csv_handler.query_csv,
    description="Retrieve patient medical history from structured CSV records."
)

serpapi_tool = Tool(
    name="Real-Time Healthcare Search",
    func=search_health_info,
    description="Fetch the latest healthcare updates and research from the web."
)

pdf_faiss_tool = Tool(
    name="Healthcare PDF Search",
    func=search_pdf,
    description="Retrieve information from FAISS-indexed healthcare research PDFs."
)

# ✅ List of Tools
tools = [wiki, arxiv, patient_info_tool, serpapi_tool, pdf_faiss_tool]

# ✅ Initialize LLM with Groq API
llm = ChatOpenAI(
    model=config.GEMMA_MODEL_NAME,  # ✅ From config.py
    temperature=1,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=config.GROQ_API_BASE  # ✅ Base URL from config
)

# ✅ Initialize AI Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True  # ✅ Prevent output errors
)

print("✅ Healthcare AI Chatbot is ready!")

# ✅ Optimized Response Formatter using Gemma 9B
def refine_response_with_gemma(text):
    """Formats healthcare responses clearly and concisely using Groq (Gemma 9B)."""
    prompt = f"""
    You are a **highly knowledgeable and professional Healthcare AI Assistant**.
    Your goal is to provide **clear, structured, and easy-to-read healthcare responses**.

    ### **Response Guidelines:**
    - **Keep it concise** (avoid unnecessary details and medical jargon).
    - **Use bullet points** for clarity and easy reading.
    - **Cite sources when needed** (e.g., Wikipedia, Arxiv, clinical trials).

    ### **Response Formats:**
    **1️⃣ General Health Questions:**
    ✔ **Condition:** [Short explanation]
    ✔ **Symptoms:** [Common symptoms]
    ✔ **Treatment:** [Recommended medical treatments]
    ✔ **Prevention:** [Preventive measures]
    📢 *Consult a doctor for diagnosis and treatment.*

    **2️⃣ Clinical Trial Results:**
    - **Trial Name:** [Name]
    - **Purpose:** [What is being tested?]
    - **Phase:** [1, 2, 3, or 4]
    - **Eligibility:** [Who can join?]
    - **Enrollment Status:** [Open or Closed]
    - **Source:** [Website link]

    **3️⃣ Research Paper Summary:**
    - **Title:** [Paper Title]
    - **Published On:** [Date]
    - **Authors:** [Main Authors]
    - **Summary:** [Short, easy-to-understand explanation]
    - **Source:** [Arxiv / PubMed Link]

    **4️⃣ Patient Records (CSV Data):**
    - **Patient Name:** [Name]
    - **Age:** [Age]
    - **Diagnosis:** [Condition]
    - **Last Visit:** [Date]
    - **Prescribed Medications:** [List of meds]
    📌 *For detailed history, refer to hospital records.*

    **5️⃣ PDF FAISS Retrieval (Medical Research PDFs):**
    - **Key Finding:** [Main insight from the PDF]
    - **Relevance:** [How it applies to the user's query]
    - **Source:** [PDF file reference]

    ### **Now, format the following response properly:**
    {text}
    """
    
    response = llm.invoke(prompt)
    return response.content


