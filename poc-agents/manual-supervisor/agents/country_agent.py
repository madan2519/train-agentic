from langchain.agents import create_agent
from langchain.tools import tool
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# anthropicapi_key = os.getenv("ANTHROPIC_API_KEY")

openai_api_key = os.getenv("OPENAI_API_KEY")

@tool
def get_country_details(country: str) -> str:
    """Returns basic info about a country (dummy function)."""
    return f"{country} is a country with its own government and borders."

# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=anthropicapi_key)
llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

def create_country_agent():
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are a country assistant. Use tools to answer questions."),
    #     ("human", "{input}")
    # ])

    system_message = (
        "You are a helpful country information agent. "
        "Use the provided tools to gather information about countries as needed."
    )

    tools = [get_country_details]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_message,
        name="country_agent"  # needed for langgraph-supervisor
    )
    return agent

if __name__ == "__main__":
    country_agent = create_country_agent()
    query = "I want to know about France."
    for step in country_agent.stream(
        {"messages": [{"role": "user", "content": query}]}
    ):
        for update in step.values():
            for message in update.get("messages", []):
                message.pretty_print()