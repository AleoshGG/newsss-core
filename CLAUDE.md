# NEWSSS-CORE Project Guidelines

This file outlines the architecture, principles, and rules for AI assistants and developers working on the `newsss-core` repository.

## Architecture Overview
The project follows **Clean Architecture** and **Domain-Driven Design (DDD)** principles, primarily built with **FastAPI** (HTTP framework), **Strawberry** (GraphQL), and **MCP SDK** (Model Context Protocol).

The codebase is organized into distinct layers inside `src/`:
- **`core/`**: Cross-cutting concerns (e.g., database session factory, Pydantic configuration/settings).
- **`features/<feature_name>/`**: Feature-sliced modules containing:
  - **`domain/`**: The core business logic. Includes `entities` (pure Python objects), `repositories` (abstract interfaces/protocols), and `usecases` (orchestrators of business rules).
  - **`data/`**: External data integrations. Includes repository implementations (`repository_impl.py`) and SQLAlchemy ORM models.
  - **`presentation/`**: Entry points and controllers. Includes `graphql/` (Strawberry types, queries, mutations, routers) and `mcp_tools/` (MCP tool definitions).
- **`app.py`**: The root FastAPI application that mounts the GraphQL router and the MCP streamable application.

## Core Principles

1. **Dependency Inversion**
   - Use Cases must never depend on database implementations or external API concrete classes. They should depend on abstract Repository interfaces.
   - Dependencies (like DB sessions or API keys) should be injected dynamically into Use Cases via the presentation layer (e.g., GraphQL context).

2. **Concurrency & Performance**
   - Use `asyncio` for all I/O bound operations.
   - For batch HTTP requests, utilize `httpx.AsyncClient` with connection pooling and limits, executing them concurrently via `asyncio.gather()`.

3. **Unified Transport Layer**
   - The system exposes both standard frontend interfaces (GraphQL) and AI-Agent interfaces (MCP Tools) simultaneously. Always consider how a new feature maps to both paradigms.

## Working Rules

1. **Language & Consistency**
   - Write all code, comments, docstrings, and GraphQL/MCP descriptions strictly in **English**.
   - Ensure clear, descriptive docstrings for all MCP Tools (`@mcp.tool()`) and GraphQL fields (`@strawberry.field(description=...)`), as these dictate how external agents and frontends interact with the API.

2. **Code Style**
   - Follow standard Python `PEP 8` formatting.
   - Use strict type hinting (`typing`) across all layers.
   - Treat `None` explicitly using `Optional[T]` or `T | None`.

3. **Error Handling**
   - Isolate errors during batch processing (e.g., catching exceptions inside `asyncio.gather` tasks) so that a single failure doesn't crash the entire pipeline.
   - Raise explicit `ValueError` or domain-specific exceptions in Use Cases when business constraints are violated.

4. **MCP (Model Context Protocol)**
   - MCP Tools are defined modularly in `presentation/mcp_tools/`.
   - Always import the global `mcp` instance from `src/mcp_server.py`.
   - Rely on `streamable_http_app` directly in FastAPI, and manage the `lifespan_context` manually in the FastAPI root `app.py` so the task groups initialize correctly.
