from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.features.graphql_root import graphql_app
from src.mcp_server import mcp

# Import all MCP tool modules to trigger their @mcp.tool() registration
import src.features.youtube.presentation.mcp_tools
import src.features.github.presentation.mcp_tools
import src.features.google_news.presentation.mcp_tools
import src.features.marketing.presentation.mcp_tools

# Create the MCP app with a root path for sub-mounting
mcp_app = mcp.streamable_http_app(streamable_http_path="/")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Manually initialize the MCP context (Starlette does not propagate lifespans when mounting)
    async with mcp_app.router.lifespan_context(app):
        yield


app = FastAPI(
    title="Newsss Core",
    description="GraphQL and MCP Service for YouTube, GitHub, and Google News integration.",
    lifespan=lifespan
)

# Mount the unified GraphQL router (YouTube + GitHub + Google News)
app.include_router(graphql_app, prefix="/graphql")

# Mount MCP routes (Streamable HTTP)
app.mount("/mcp", mcp_app)
