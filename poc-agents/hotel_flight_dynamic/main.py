from dotenv import load_dotenv
load_dotenv()

import operator
import os
from pydantic import BaseModel, Field
from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
# from langchain_cohere import ChatCohere
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from tools import book_hotel, book_flight


# # 2. Setup LLM
# llm = ChatCohere(model="command-a-03-2025", temperature=0, api_key=os.getenv("COHERE_API_KEY"))

# 1. Initialize Ollama LLM with Gemma 3
# llm = ChatOllama(
#     model="functiongemma",
#     temperature=0, # Keep temp at 0 for more reliable tool calls
# )

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Define Sub-Agents
# Note: These are compiled graphs themselves
hotel_agent_sub = create_react_agent(llm, tools=[book_hotel], prompt=(
        "You are a Hotel Booking Specialist. You can ONLY handle hotel-related tasks. "
        "If the user's destination is mentioned in the history, use it. "
        "Otherwise, ask for the city name."
    ))
flight_agent_sub = create_react_agent(llm, tools=[book_flight], prompt="You are a Flight Specialist. Handle all plane and travel reservation queries.")

# 4. Define Workflow State
class AgentState(TypedDict):
    # Annotated + operator.add is REQUIRED to merge messages
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 5. Define Node Functions
# These wrappers are the "bridge" that makes the code work
def call_hotel(state: AgentState):
    response = hotel_agent_sub.invoke(state)
    return {"messages": response["messages"]}

def call_flight(state: AgentState):
    response = flight_agent_sub.invoke(state)
    return {"messages": response["messages"]}

# 6. Define Router
# def router(state: AgentState):
#     last_message = state["messages"][-1].content.lower()
#     if "hotel" in last_message:
#         return "hotel_agent"
#     elif "flight" in last_message:
#         return "flight_agent"
#     return END

class Route(BaseModel):
    """Decide which agent to route to based on user intent."""
    next_node: Literal["hotel_agent", "flight_agent", "finish"] = Field(
        description="The name of the next node to call. Choose 'finish' if the query is general or already answered."
    )

router_llm = llm.with_structured_output(Route)

def router(state: AgentState):
    """An LLM-based router that understands context."""
    system_prompt = (
        "You are an expert travel router. Look at the conversation history and "
        "decide if the user's latest request is about hotel booking, flight booking, "
        "or if the task is complete. "
        "If the user says 'stay', 'room', or 'accommodation', route to hotel_agent. "
        "If the user says 'travel', 'trip', or 'fly', route to flight_agent."
    )
    
    # Pass the whole message history for context
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    decision = router_llm.invoke(messages)
    
    if decision.next_node == "hotel_agent":
        return "hotel_agent"
    elif decision.next_node == "flight_agent":
        return "flight_agent"
    return END

# 7. Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("hotel_agent", call_hotel)
workflow.add_node("flight_agent", call_flight)

workflow.add_conditional_edges(START, router)

workflow.add_edge("hotel_agent", END)
workflow.add_edge("flight_agent", END)

app = workflow.compile()

# from langchain_core.messages import HumanMessage
# from agents import app

def run_workflow(query: str):
    inputs = {"messages": [HumanMessage(content=query)]}
    
    print("DEBUG: Sending request to Graph...")
    # Using stream_mode="updates" to see state changes as they happen
    for event in app.stream(inputs, stream_mode="updates"):
        for node_name, state_update in event.items():
            print(f"\n[ACTIVE NODE: {node_name}]")
            
            # Print messages from this node
            if "messages" in state_update:
                for msg in state_update["messages"]:
                    if msg.type != "human":
                        msg.pretty_print()

if __name__ == "__main__":
    print("--- Hotel Request ---")
    # run_workflow("I want to book a hotel in Paris")
    result = run_workflow("I need an accomidation in Paris for 3 days.")
    # print(result)
    # run_workflow("I want to book a hotel in New York for 5 nights.")
    # run_workflow("I want to book a flight to Canada")
    
    # print("\n--- Flight Request ---")
    # run_workflow("Find me a flight to London")