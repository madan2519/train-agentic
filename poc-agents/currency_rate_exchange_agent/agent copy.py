from dotenv import load_dotenv
import os

# Load environment variables from a .env file (if present)
load_dotenv()
# Replace 'YOUR_OPENAI_API_KEY' with your actual key if not set as env var
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# ---------------------------------------------------------------------------
# Ensure the key is set before proceeding
# if "OPENAI_API_KEY" not in os.environ:
#     print("Please set the OPENAI_API_KEY environment variable.")

if "COHERE_API_KEY" not in os.environ:
    print("Please set the COHERE_API_KEY environment variable.")

# from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere

# Initialize the LLM (using a powerful model is recommended for ReAct)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

llm = ChatCohere(model="command-a-03-2025", temperature=0)

# ---------------------------------------------------------------------------
# from langchain.agents.react.base import create_react_agent
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
# from langchain_core.messages import HumanMessage, SystemMessage
from tools import tools

# Single source of truth for the system prompt used by both the agent prompt
# and direct model invocation helper. This avoids duplicating the same text.
SYSTEM_CONTENT = """
Answer the user's question using these tools:
{tools}

Available tool names: [{tool_names}]

Format:
Thought: Always think about what to do.
Action: The tool to use (must be one of [{tool_names}]).
Action Input: The input to the tool.
Observation: The tool output.
... (repeat if needed)
Thought: I now know the final answer.
Final Answer: The final response to the user.

Question: {input}j
Thought: {agent_scratchpad}
"""

# 2. Create the Prompt
prompt = PromptTemplate.from_template(SYSTEM_CONTENT)

# 3. Define your actual tool objects (not just names)
# tools = [your_currency_tool, search_tool]

# 4. Create the Agent 
# Pass the actual tool list, not just names. LangChain will fill {tool_names} for you.
agent = create_react_agent(llm, tools, prompt)

# 5. Create the Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools, # Pass the tool objects here
    verbose=True,
    handle_parsing_errors=True,
)

# ---------------------------------------------------------------------------
# Example: build messages with SystemMessage and HumanMessage for direct
# model invocation. This is useful if you want to call the chat model
# directly instead of using the agent loop. The system content mirrors the
# agent system prompt and documents the `latest_exchange_rates` tool.
# def build_invoke_messages(user_input: str):
#     """Return a list of SystemMessage and HumanMessage for direct model invocation.

#     This uses the same `SYSTEM_CONTENT` used by the agent prompt so there is a
#     single source of truth for system instructions.
#     """
#     messages = [
#         SystemMessage(content=SYSTEM_CONTENT),
#         HumanMessage(content=user_input),
#     ]

#     return messages