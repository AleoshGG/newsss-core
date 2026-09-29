from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.features.youtube.presentation.graphql.router import graphql_app
from src.mcp_server import mcp

# Import the youtube tools to register them in the 'mcp' instance
import src.features.youtube.presentation.mcp_tools

# Create the MCP app with a root path for sub-mounting
mcp_app = mcp.streamable_http_app(streamable_http_path="/")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Manually initialize the MCP context (Starlette does not propagate lifespans when mounting)
    async with mcp_app.router.lifespan_context(app):
        yield

app = FastAPI(
    title="Neurotry YouTube Service",
    description="GraphQL and MCP Service for YouTube integration.",
    lifespan=lifespan
)

# Mount the GraphQL router
app.include_router(graphql_app, prefix="/graphql")

# Mount MCP routes (Streamable HTTP)
app.mount("/mcp", mcp_app)


