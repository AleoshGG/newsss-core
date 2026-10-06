from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.features.graphql_root import graphql_app
from src.mcp_server import mcp

# Import all MCP tool modules to trigger their @mcp.tool() registration
import src.features.documentation.presentation.mcp_tools
import src.features.youtube.presentation.mcp_tools
import src.features.github.presentation.mcp_tools
import src.features.google_news.presentation.mcp_tools
import src.features.marketing.presentation.mcp_tools
from mcp.server.transport_security import TransportSecuritySettings
from src.core.config import settings

# Lista de hosts permitidos (local + Railway si existe)
allowed = ["127.0.0.1", "localhost"]
if settings.RAILWAY_PUBLIC_DOMAIN:
    allowed.append(settings.RAILWAY_PUBLIC_DOMAIN)

# Create the MCP app with a root path for sub-mounting
mcp_app = mcp.streamable_http_app(
    streamable_http_path="/",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=allowed
    )
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Manually initialize the MCP context (Starlette does not propagate lifespans when mounting)
    async with mcp_app.router.lifespan_context(app):
        yield


from fastapi.middleware.cors import CORSMiddleware
from src.core.security import SecurityMiddleware

app = FastAPI(
    title="Newsss Core",
    description="GraphQL and MCP Service for YouTube, GitHub, and Google News integration.",
    lifespan=lifespan
)

# 1. CORS Middleware
# Parse CORS_ORIGINS from settings
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Security Middleware (Rate limit + Auth)
app.add_middleware(SecurityMiddleware)

# Mount the unified GraphQL router (YouTube + GitHub + Google News)
app.include_router(graphql_app, prefix="/graphql")

# Mount MCP routes (Streamable HTTP)
app.mount("/mcp", mcp_app)
