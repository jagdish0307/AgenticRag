# This script is designed to test the agent's functionality by sending various queries and printing the responses.
import config
from agent import agent_executor, refine_response_with_gemma

def test_agent():
    queries = [
        "What are the symptoms of diabetes?",
        "Retrieve patient Blood type of Brooke Brady.",
        "Find latest AI advancements in healthcare.",
        "Summarize a research paper on heart disease.",
        "Latest treatments for diabetes in 2024",
        "How Ethical Challenges Can Arise in Public Health Research pdf: Lessons Learned from Cases",
        "What are the ethical concerns in medical AI?"
    ]
    
    print("\n🚀 Running Agent Tests...\n")

    for query in queries:
        print(f"\n📝 **Query:** {query}")
        
        # ✅ Query the Agent
        raw_response = agent_executor.invoke({"input": query})
        
        # ✅ Format the Response Using Gemma 9B
        formatted_response = refine_response_with_gemma(raw_response["output"])
        
        print("\n🔹 **AI Response:**\n", formatted_response)

    print("\n✅ **All Agent Tests Completed Successfully!**")

if __name__ == "__main__":
    test_agent()


