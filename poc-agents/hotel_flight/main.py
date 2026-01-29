from langchain_core.messages import HumanMessage
from multi_agent_basic import app

def run_workflow(query: str):
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # Using stream_mode="values" to see the results
    for event in app.stream(inputs, stream_mode="values"):
        # This will print every message as it is added to the state
        message = event["messages"][-1]
        if message.type != "human": # Skip printing the question again
            message.pretty_print()

def main():
    # Example: This will go to Flight Agent FIRST, then Hotel Agent
    print("--- Hotel Request ---")
    run_workflow("I want to book a hotel in Paris")
    # print("\n--- Flight Request ---")
    # run_workflow("I want to book a flight to Canada")

if __name__ == "__main__":
    main()
