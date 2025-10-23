from typing import Any
import httpx
# from mcp.server.fastmcp import FastMCP
import DaiCCore

# Initialize FastMCP server
# mcp = FastMCP("daic")

# @mcp.tool()
def open_alert() -> None:
    """
    Open an alert in daic
    """
    input = DaiCCore.input_dialog("Prompt:")
    print(input)

DaiCCore.register("MCPServer", "MCPServer that expose DaiCCore functions", lambda: mcp.run(transport='stdio'))
