from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

@tool
def get_weather(city: str) -> str:
    """Returns weather for a city (dummy function)."""
    return f"The weather in {city} is 30°C and sunny."

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)


def create_weather_agent():
    system_message = (
        "You are a helpful weather information agent. "
        "Use the provided tools to gather weather information as needed."
    )

    tools = [get_weather]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_message,
        name="weather_agent"
    )
    return agent

if __name__ == "__main__":
    weather_agent = create_weather_agent()
    query = "What is the weather in Paris?"
    for step in weather_agent.stream(
        {"messages": [{"role": "user", "content": query}]}
    ):
        for update in step.values():
            for message in update.get("messages", []):
                message.pretty_print()