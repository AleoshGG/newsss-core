# Changelog

All notable changes to the NEWSSS-CORE server will be documented in this file.

## [0.0.2] - 2026-09-29

### Added
- **Config-Driven Architecture**: Each data source (YouTube, GitHub, Google News) now has a singleton configuration table in the database (`id=1`). Configs are auto-created with sensible defaults on first use — no Alembic seed required.
  - New tables: `youtube_search_config`, `github_search_config`, `google_news_config`.
- **GitHub Feature — Full Implementation**:
  - `GitHubFetcherUseCase`: Reads config from DB, searches repos concurrently per topic via GitHub API (`GET /search/repositories`), applies post-API filters (language, stars, forks, license), and fetches READMEs concurrently.
  - `ReadRecentGitHubReposUseCase`: Retrieves repos from the local DB ordered by `updated_at`.
  - `UpdateGitHubConfigUseCase`: UPSERT for the GitHub search config singleton.
  - GraphQL: `getRecentGithubRepos`, `getGithubConfig` queries; `fetchAndSaveGithubRepos`, `updateGithubConfig` mutations.
  - MCP Tools: `fetch_github_repos()` and `get_recent_github_repos(limit, offset)`.
- **Google News Feature — Full Implementation**:
  - `GoogleNewsFetcherUseCase`: Reads config from DB, fetches two RSS feeds concurrently (configured language + English AI fallback via `feedparser`), scrapes `og:image` and article text using `BeautifulSoup` + `lxml`.
  - `ReadRecentNewsArticlesUseCase`: Retrieves articles from the local DB ordered by `fetched_at`.
  - `UpdateGoogleNewsConfigUseCase`: UPSERT for the Google News config singleton.
  - GraphQL: `getRecentNewsArticles`, `getGoogleNewsConfig` queries; `fetchAndSaveNewsArticles`, `updateGoogleNewsConfig` mutations.
  - MCP Tools: `fetch_google_news_articles()` and `get_recent_news_articles(limit, offset)`.
- **YouTube Config Management**:
  - `UpdateYouTubeConfigUseCase`: UPSERT for the YouTube search config singleton.
  - GraphQL: `getYoutubeConfig` query and `updateYoutubeConfig` mutation.
- **Unified GraphQL Schema**: All three features merged into a single Strawberry schema via multiple inheritance (`features/graphql_root.py`), backed by a single FastAPI router with independent DB sessions per feature.
- **New Dependencies**: `feedparser`, `beautifulsoup4`, `lxml`.
- **Optional `GITHUB_TOKEN`**: Added to `Settings` to raise GitHub API rate limit from 60 to 5,000 requests/hour.

### Changed
- **YouTube Fetcher refactored (breaking)**: `YouTubeFetcherUseCase.execute()` no longer accepts a `config` argument — it loads the search configuration automatically from the database via `repository.get_config()` and updates `last_search_at` after each fetch.
- **`fetchAndSaveYoutubeVideos` GraphQL mutation**: Removed the `config` input argument — configuration is now read from the DB.
- **`fetch_youtube_videos` MCP tool**: Removed all parameters — configuration is now read from the DB.
- **Repository interfaces extended**: `YouTubeRepository`, `GitHubRepository`, and `GoogleNewsRepository` now declare `get_config()`, `save_config()`, and `find_recent()` abstract methods.
- **GraphQL context**: Each feature repository now gets its own independent `AsyncSession` to avoid SQLAlchemy concurrent-operation errors.

## [0.0.1] - 2026-09-29

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

