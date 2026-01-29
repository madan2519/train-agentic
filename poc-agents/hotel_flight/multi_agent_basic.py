import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI # Using OpenAI as per your update
from dotenv import load_dotenv
from tools import book_hotel, book_flight

load_dotenv()

# 2. Setup LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Define Sub-Agents
# These agents stay specialized to their own tools
flight_agent_sub = create_react_agent(llm, tools=[book_flight])
hotel_agent_sub = create_react_agent(llm, tools=[book_hotel])

# 4. Define Workflow State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 5. Node Wrappers
def call_flight(state: AgentState):
    # This node only handles flight logic
    response = flight_agent_sub.invoke(state)
    return {"messages": response["messages"]}

def call_hotel(state: AgentState):
    # This node only handles hotel logic
    response = hotel_agent_sub.invoke(state)
    return {"messages": response["messages"]}

# 6. Build Sequential Graph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("flight_agent", call_flight)
workflow.add_node("hotel_agent", call_hotel)

# --- THE SEQUENTIAL LOGIC ---
# Step 1: Always start with the Flight Agent
workflow.set_entry_point("flight_agent")

# Step 2: Once Flight Agent finishes, always go to Hotel Agent
workflow.add_edge("flight_agent", "hotel_agent")

# Step 3: Once Hotel Agent finishes, end the workflow
workflow.add_edge("hotel_agent", END)

app = workflow.compile()