
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

# -------------------------------------------------------------------
# 1. Create MCP client using HTTP URL (Way 2)
# -------------------------------------------------------------------

client = MultiServerMCPClient({
    "my_server": {
        "url": "http://127.0.0.1:8000/mcp",
        "transport": "http"
    }
})

# Discover tools exposed by the MCP server
tools = asyncio.run(client.get_tools())

print("Available tools:", [tool.name for tool in tools])

# -------------------------------------------------------------------
# 2. Initialize LLM
# -------------------------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------------------------------------------------
# 3. System prompt (tight, deterministic)
# -------------------------------------------------------------------

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

# -------------------------------------------------------------------
# 5. Run example
# -------------------------------------------------------------------

# if __name__ == "__main__":
#     result = agent.invoke(
#         {"input": "What is the current exchange rate from USD to EUR?"}
#     )

#     # Extract final AI answer
#     final_answer = None
#     for msg in reversed(result["messages"]):
#         if msg.type == "ai" and msg.content:
            # final_answer = msg.content
            # break

#     print("\nFinal Answer:")
#     print(final_answer)
