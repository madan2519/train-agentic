import os
from dotenv import load_dotenv

load_dotenv()


import json
import requests
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("currency-tools")

@mcp.tool()
def latest_exchange_rates(base: str = "USD", symbols: Optional[str] = None) -> dict:
    """
    Return latest exchange rates from CurrencyBeacon.
    """

    api_key = os.environ.get("CURRENCY_BEACON_API_KEY")
    print("Beacon API Key:", api_key)
    if not api_key:
        return {"error": "CURRENCY_BEACON_API_KEY not set"}

    params = {
        "api_key": api_key,
        "base": base
    }

    if symbols:
        params["symbols"] = symbols

    url = "https://api.currencybeacon.com/v1/latest"

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return {
            "base": data.get("base"),
            "rates": data.get("rates"),
            "date": data.get("date")
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------------------------------------------
# Run the MCP server with stdio transport
# -------------------------------------------------------------------

# if __name__ == "__main__":
#     api_key = os.environ.get("CURRENCY_BEACON_API_KEY")
#     print("Beacon API Key:", api_key)
#     print("MCP Currency Server started. Waiting for clients...")
#     mcp.run()

# ---------------------------------------------------------------------------
# To run with HTTP transport
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http", mount_path="/mcp")