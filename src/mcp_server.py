from mcp.server.mcpserver import MCPServer

# Instancia global del servidor MCP
mcp = MCPServer(
    "neurotry-mcp",
    instructions=(
        "Call get-documentation-mcp with no arguments to learn how to select "
        "tools for the user's intent and follow supported workflows, including "
        "Daily: fetch GitHub, Google News, and YouTube data, run the ML "
        "marketing pipeline, and show campaigns."
    ),
)
