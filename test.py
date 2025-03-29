
from agent import agent_executor
from agent import refine_response_with_gemma


# ✅ Query the Agent
while True:
    query = input("\n🩺 Enter your healthcare query (or type 'exit' to quit): ")
    if query.lower() == "exit":
        print("\n👋 Exiting... Stay healthy!")
        break
    
    # ✅ Query the Agent
    raw_response = agent_executor.invoke({"input": query})
    
    # ✅ Format the Response Using Gemma 2B
    detailed_response = refine_response_with_gemma(raw_response["output"])
    
    print("\n🔹 Easy-to-Read Healthcare Info:\n", detailed_response)



