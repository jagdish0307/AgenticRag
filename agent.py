# import sys
# from retrieval import retrieve_info

# def main():
#     print("🤖 Healthcare Agent Initialized!")
#     print("Type your query or type 'exit' to quit.\n")

#     while True:
#         # Get user input
#         user_query = input("📝 Enter your query: ").strip()
#         if user_query.lower() == "exit":
#             print("👋 Exiting Healthcare Agent. Have a great day!")
#             sys.exit()

#         # Ask if patient-related info is needed
#         patient_query = input("🔍 Do you need patient records? (Enter patient name or press Enter to skip): ").strip()
#         use_llm = input("💡 Would you like an AI-generated response? (yes/no): ").strip().lower() == "yes"

#         # Retrieve information
#         results = retrieve_info(user_query, patient_query if patient_query else None, use_llm=use_llm)

#         # Display results
#         print("\n📌 **Results:**")
#         for key, value in results.items():
#             print(f"\n🔹 {key}: {value}")

# if __name__ == "__main__":
#     main()


import sys
from retrieval import retrieve_info

def format_response(results):
    """Formats results in a simple, chat-like format."""
    response = ""
    
    if results.get("LLM Response") and results["LLM Response"] != "LLM response disabled.":
        return results["LLM Response"]["response"]
    
    if results.get("Patient Data") and isinstance(results["Patient Data"], list):
        response += "\n📌 Patient Records:\n"
        for record in results["Patient Data"]:
            response += f"🔹 {record['name']} - Blood Type: {record['blood_type']}, Condition: {record['medical_condition']}, Doctor: {record['doctor']}, Hospital: {record['hospital']}\n"
        return response.strip()
    
    if results.get("FAISS Results") and results["FAISS Results"]:
        response += "\n📌 Hospital Policies:\n"
        response += "\n".join(results["FAISS Results"])
        return response.strip()
    
    if results.get("Clinical Trials") and results["Clinical Trials"].get("studies"):
        response += "\n📌 Latest Clinical Trials:\n"
        response += "\n".join(str(study) for study in results["Clinical Trials"]["studies"])
        return response.strip()
    
    if results.get("PubMed Articles") and results["PubMed Articles"]["esearchresult"]["idlist"]:
        response += "\n📌 Research Articles:\n"
        response += "\n".join(results["PubMed Articles"]["esearchresult"]["idlist"])
        return response.strip()
    
    return "❌ No relevant information found. Please try another query."

def main():
    print("🤖 Healthcare Agent Initialized!")
    print("Type your query or type 'exit' to quit.\n")

    while True:
        user_query = input("📝 Enter your query: ").strip()
        if user_query.lower() == "exit":
            print("👋 Exiting Healthcare Agent. Have a great day!")
            sys.exit()

        patient_query = input("🔍 Do you need patient records? (Enter patient name or press Enter to skip): ").strip()
        use_llm = input("💡 Would you like an AI-generated response? (yes/no): ").strip().lower() == "yes"

        results = retrieve_info(user_query, patient_query if patient_query else None, use_llm=use_llm)
        response = format_response(results)
        
        print("\n" + response + "\n")

if __name__ == "__main__":
    main()
