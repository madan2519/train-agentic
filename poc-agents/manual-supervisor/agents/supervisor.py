from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from agents.country_agent import create_country_agent
from agents.weather_agent import create_weather_agent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

# Create the subagents
country_agent = create_country_agent()
weather_agent = create_weather_agent()


# Wrap subagents as tools
@tool
def get_country_info(request: str) -> str:
    """Get information about a country using natural language.
    
    Use this when the user wants to know about a specific country, its details,
    geography, or other country-related information.
    
    Input: Natural language request about a country (e.g., 'Tell me about France')
    """
    result = country_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].content


@tool
def get_weather_info(request: str) -> str:
    """Get weather information for a location using natural language.
    
    Use this when the user wants to know about weather conditions, temperature,
    or weather forecasts for a specific city or location.
    
    Input: Natural language request about weather (e.g., 'What is the weather in Paris?')
    """
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].content


def create_supervisor_agent():
    """Create the supervisor agent that coordinates weather and country subagents."""
    
    system_message = (
        "You are a helpful personal assistant supervisor. "
        "You can provide information about countries and weather conditions. "
        "You have access to two specialized agents: "
        "1. A country information agent - for details about countries "
        "2. A weather agent - for weather information "
        "Route user requests to the appropriate agent(s) based on their query. "
        "When a request involves multiple actions, use multiple tools in sequence. "
        "Synthesize the results and provide a coherent response to the user."
    )

    tools = [get_country_info, get_weather_info]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_message,
        name="supervisor_agent"
    )
    return agent

