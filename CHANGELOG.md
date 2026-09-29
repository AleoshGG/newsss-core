# Changelog

All notable changes to the NEWSSS-CORE server will be documented in this file.

## [Unreleased]

### Added
- **YouTube Fetcher Pipeline**: Implemented a concurrent fetching pipeline (`YouTubeFetcherUseCase`) to search for YouTube videos, enrich metrics, and extract transcripts efficiently using `httpx` and `youtube-transcript-api`.
- **Database Persistence**: Integrated SQLAlchemy repository to save and retrieve parsed YouTube videos (`YouTubeRepositoryImpl`).
- **GraphQL Presentation Layer**: Added a Strawberry GraphQL integration with FastAPI to expose the YouTube use cases (`getRecentYoutubeVideos` query and `fetchAndSaveYoutubeVideos` mutation).
- **MCP (Model Context Protocol) Server**: Integrated Anthropic's MCP SDK to expose backend capabilities as tools for AI agents.
  - Deployed `streamable_http_app` directly in FastAPI, sharing the same port as the main server.
  - Registered `fetch_youtube_videos` and `get_recent_youtube_videos` tools.

### Changed
- Configured dynamic dependency injection for the database session and API keys into GraphQL and MCP context layers.
- Translated project docstrings, API descriptions, and inline comments to English for codebase consistency.
