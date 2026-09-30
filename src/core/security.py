import time
from collections import defaultdict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.core.config import settings

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Simple in-memory structure: { "ip_address": [timestamp1, timestamp2] }
        self.rate_limit_records = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # 1. Rate Limiting (Basic & Functional)
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean timestamps older than 60 seconds
        self.rate_limit_records[client_ip] = [
            t for t in self.rate_limit_records[client_ip] 
            if now - t < 60
        ]
        
        if len(self.rate_limit_records[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
        
        self.rate_limit_records[client_ip].append(now)

        # 2. Authentication
        api_key = settings.APP_API_KEY
        
        # MCP Auth: query param
        if request.url.path.startswith("/mcp"):
            if request.query_params.get("api_key") != api_key:
                return JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid or missing API Key in URL"})
                
        # GraphQL Auth: header
        elif request.url.path.startswith("/graphql"):
            # Attempt to extract from x-api-key or Authorization (Bearer <key>)
            provided_key = request.headers.get("x-api-key")
            if not provided_key:
                auth_header = request.headers.get("authorization", "")
                if auth_header.lower().startswith("bearer "):
                    provided_key = auth_header[7:]
                    
            if provided_key != api_key:
                return JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid or missing API Key in Headers"})

        # Allow request to proceed
        return await call_next(request)
