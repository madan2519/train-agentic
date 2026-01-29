from agent import agent_executor

# --- Example 1: Using the currency tool (USD -> INR) ---
print("\n--- Running Example 1 (Currency Tool: USD -> INR) ---")
result_1 = agent_executor.invoke({"input": "What is the current exchange rate from USD to INR?"})
print(f"Final Answer: {result_1['output']}")

# --- Example 2: Using the search tool ---
# print("\n--- Running Example 2 (Search Tool) ---")
# result_2 = agent_executor.invoke({"input": "What is the largest city in the world by population?"})
# print(f"Final Answer: {result_2['output']}")