from xmlrpc import client
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

client = MultiServerMCPClient({
    "my_server": {
        "command": "python",
        "args": ["currency_mcp_server.py"],
        "transport": "stdio",
    }
})

# Get tools from all connected servers
tools = asyncio.run(client.get_tools())


# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

SYSTEM_PROMPT = """
You are a financial assistant.

Rules:
- If the user asks for an exchange rate and mentions both currencies,
  ALWAYS call latest_exchange_rates.
- Never ask follow-up questions if currencies are provided.
- Use the tool output to answer with a numeric rate.

Answer clearly and concisely.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

# if __name__ == "__main__":
#     result = agent.invoke(
#         {"input": "What is the current exchange rate from USD to EUR?"}
#     )

#     # Extract final answer
#     for msg in reversed(result["messages"]):
#         if msg.type == "ai" and msg.content:
#             print("\nFinal Answer:")
#             print(msg.content)
#             break
