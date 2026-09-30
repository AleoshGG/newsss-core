# Changelog

All notable changes to the NEWSSS-CORE server will be documented in this file.

## [0.0.4] - 2026-09-30

### Added
- **Security Middleware & Rate Limiting**: Added a custom `SecurityMiddleware` for the FastAPI application to protect endpoints ahead of testing phase deployment.
  - Implements an in-memory sliding window rate limiter (100 requests per minute per IP) to prevent abuse.
  - Secures GraphQL endpoints (`/graphql`) by requiring an `X-API-Key` or `Authorization` header.
  - Secures MCP endpoints (`/mcp`) by requiring an `api_key` URL query parameter.
- **CORS Support**: Integrated FastAPI's `CORSMiddleware` with configurable allowed origins via the `.env` file.
- **Medallion Architecture (Silver Layer)**: Implemented a staging table `normalized_items` to store cleaned and translated items. This splits the marketing pipeline into two resilient phases:
  - Phase 1 (Clean & Translate): Translates items and gracefully handles LLM failures (e.g., saving successfully translated items before aborting).
  - Phase 2 (Generate Campaigns): Reads translated items, clusters them, and generates campaigns. This avoids losing LLM tokens if the pipeline fails downstream.
- **Message Queue Flow for Sources**: Added an `is_processed` boolean column to all raw source tables (`youtube_videos`, `github_data`, `google_news_articles`). The pipeline now only consumes un-processed items and marks them as processed upon successful ingestion into the Silver Layer, preventing duplicate translations.
- **Full Google News Article Extraction**: Integrated `googlenewsdecoder` to resolve base64 Google News redirect URLs (`CBMi...`) to the actual publisher URLs, enabling full HTML content scraping via BeautifulSoup (with RSS summaries as a fallback).
- **Environment-driven Gemini Model**: Extracted the Gemini model name to a configurable environment variable (`GEMINI_MODEL`) in `.env` and `Settings`, defaulting to `gemini-3.8-flash` following Google's model deprecation.

### Changed
- **GitHub README Fetching**: Switched from `api.github.com` endpoints (which hit strict 60 req/hr limits and 403s) to direct RAW downloads from `raw.githubusercontent.com` with branch fallbacks (`main`/`master`).
- **YouTube API Syntax**: Updated `youtube-transcript-api` calls to use the modern instance syntax (`YouTubeTranscriptApi().list(video_id)`) with a multi-language fallback strategy.
- **Run Marketing Pipeline Orchestrator**: Refactored to operate over the new Silver Layer, efficiently grouping data from multiple scraper runs into a single semantic clustering batch.

## [0.0.3] - 2026-09-30

### Added

- **Marketing Feature — ML Pipeline for Digital Marketing Campaigns**:
  A new `src/features/marketing/` feature that orchestrates a 5-stage ML + LLM pipeline over the ingested data (YouTube, GitHub, Google News) to generate B2B marketing campaigns targeting consultancies and enterprise decision-makers.

  **Stage 0+1 — Data Cleaning & Normalization** (`CleanAndNormalizeUseCase`, `DataCleaner`):
  - Source-aware cleaning handles the real-world quality issues of each data source:
    - **YouTube**: Detects and discards absent transcripts (literal `"Transcript not available"` strings and variants); strips auto-caption noise tags (`[Music]`, `[Applause]`).
    - **GitHub**: Strips markdown syntax from READMEs — fenced code blocks, badge images, tables, headers, HTML tags, and list markers — leaving clean prose. Falls back to the repo `description` if the cleaned README is too short.
    - **Google News**: Detects captcha/paywall fingerprints in scraped content (`"Please enable JavaScript"`, `"Subscribe to continue"`, etc.) and discards poisoned articles. Falls back to the article title if content is absent but the title is long enough.
  - Language detection via `langdetect` (offline, no API cost); non-English items are translated to English using the configured LLM before clustering.
  - Returns a `CleaningStats` struct exposing the number of items fetched, discarded, translated, and passed per source — surfaced in the GraphQL and MCP responses.

  **Stage 2 — B2B Intent Filtering** (`IntentFilterUseCase`):
  - Scores each `NormalizedItem` with a weighted formula: keyword match score × 0.50 + normalized engagement × 0.30 + recency decay × 0.20.
  - Keyword taxonomy calibrated for tech consultancies (high-intent: `enterprise`, `saas`, `ai agent`, `llm`, `launch`, `case study`, `digital transformation`; low-intent: `bugfix`, `refactor`, `version bump`).
  - Items below a configurable `min_intent_score` threshold (default `0.25`) are discarded.

  **Stage 3 — Semantic Clustering** (`ClusterContentUseCase`):
  - Generates dense semantic embeddings locally using `sentence-transformers` (`all-MiniLM-L6-v2`, ~90 MB, cached after first run — no GPU required).
  - Groups items into K topic clusters using K-Means (`scikit-learn`). Auto-reduces cluster count if fewer items than requested clusters are available.
  - Extracts representative TF-IDF keywords per cluster for automatic topic labeling.
  - All CPU-bound computation offloaded to a thread pool via `asyncio.to_thread` to avoid blocking FastAPI's event loop.

  **Stage 4 — LLM Content Generation** (`GenerateMarketingContentUseCase`):
  - Generates structured marketing campaigns per cluster using the configured LLM.
  - Three campaign formats with dedicated B2B prompt templates: `linkedin_post`, `twitter_thread`, `email_newsletter`.
  - Prompts are calibrated for a consulting/enterprise audience (professional tone, no buzzwords, actionable insights, clear CTA).
  - Robust JSON parsing with graceful fallback if the LLM returns non-JSON output.
  - Cluster generation calls are concurrent via `asyncio.gather`; errors in individual clusters are isolated and do not abort the pipeline.

  **Orchestrator** (`RunMarketingPipelineUseCase`):
  - Chains all five stages and persists results (`content_clusters`, `marketing_campaigns`) to PostgreSQL.
  - Returns a `PipelineResult` with campaigns, cluster count, item counts at each stage, and `CleaningStats`.

  **New DB tables** (via Alembic autogenerate migration `6ae5d0b4ff03`):
  - `content_clusters` — semantic topic clusters from each pipeline run.
  - `marketing_campaigns` — LLM-generated campaigns with `status` (`draft` / `approved` / `published`).

  **GraphQL** (`MarketingQuery`, `MarketingMutation` merged into unified schema):
  - `runMarketingPipeline(limitPerSource, nClusters, minIntentScore, campaignType, translateNonEnglish)` mutation.
  - `getMarketingCampaigns(limit, status)` and `getContentClusters(limit)` queries.
  - `PipelineResultType` exposes campaigns + `CleaningStatsType` for observability.

  **MCP Tools**:
  - `run_marketing_pipeline(limit_per_source, n_clusters, campaign_type, translate_non_english)` — triggers the full pipeline.
  - `get_marketing_campaigns(limit, status)` — reads stored campaigns with optional status filter.

- **Abstract LLM Interface** (`src/core/llm/`):
  - `LLMClient` — abstract base class enabling any LLM provider to be swapped in without modifying business logic.
  - `GeminiLLMClient` — default implementation using the `google-genai` SDK (`gemini-2.0-flash`).
  - `translate_to_english()` method used by the cleaning stage for multilingual content normalization.

- **New Settings**: `GEMINI_API_KEY: str | None` added to `Settings` — required to run the marketing pipeline.

- **New Dependencies**: `sentence-transformers`, `scikit-learn`, `numpy`, `langdetect`, `google-genai`.

### Changed

- **Unified GraphQL Schema** extended: `MarketingQuery` and `MarketingMutation` merged into `Query` and `Mutation` root types via multiple inheritance. `marketing_repository` and `llm` injected into the shared GraphQL context (with a lazy import guard so the server remains startable without `GEMINI_API_KEY`).
- **`src/app.py`**: Imports `src.features.marketing.presentation.mcp_tools` to register the two new MCP tools at startup.
- **`src/core/db/base.py`**: Imports `ContentClusterModel` and `MarketingCampaignModel` so Alembic's autogenerate detects the new tables.

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

