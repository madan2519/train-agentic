import asyncio
# from agent import agent
from agent_http_mcp import agent as http_agent  


async def main():
    # --- Example 1: Using the MCP agent (local process) ---
    # result = await agent.ainvoke(
    #     {"input": "What is the current exchange rate from USD to INR?"}
    # )

    # --- Example 2: Using the HTTP MCP agent ---

    result = await http_agent.ainvoke(
        {"input": "What is the current exchange rate from USD to EUR?"}
    )

    # # Extract final AI answer
    final_answer = None
    print(result)
    for msg in reversed(result["messages"]):
        if msg.type == "ai" and msg.content:
            final_answer = msg.content
            break

    print("\nFinal Answer:")
    print(final_answer)


if __name__ == "__main__":
    asyncio.run(main())