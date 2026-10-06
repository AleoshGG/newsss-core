from mcp.types import ToolAnnotations

from src.mcp_server import mcp


MCP_DOCUMENTATION = """\
# MCP tool selection and workflows

This guide describes how an agent should call the available tools. Reading it
does not execute a workflow, fetch data, or generate campaigns. Use the exact
tool names below and match the user's intent before performing any action.

## Choose tools by intent

| User intent | Tools and behavior |
| --- | --- |
| Run the Daily / daily workflow / daily marketing routine | Follow the complete Daily workflow below. |
| Refresh or fetch GitHub repositories | `fetch_github_repos` writes fetched repositories to the database. |
| Refresh or fetch Google News articles | `fetch_google_news_articles` writes fetched articles to the database. |
| Refresh or fetch YouTube videos | `fetch_youtube_videos` writes fetched videos to the database. |
| Show saved GitHub repositories | `get_recent_github_repos` reads stored repositories. |
| Show saved Google News articles | `get_recent_news_articles` reads stored articles. |
| Show saved YouTube videos | `get_recent_youtube_videos` reads stored videos. |
| Run ML / generate campaigns from stored data | `run_marketing_pipeline` processes stored pending data and saves draft campaigns. |
| Show existing campaigns | `get_marketing_campaigns` reads saved campaigns; no fetching or generation is needed. |

If the user asks for fresh source data to be displayed, fetch that source and
then call its corresponding reader. Readers alone do not refresh external data.
For ambiguous requests, clarify whether the user wants saved results or a new
run. Do not infer the complete Daily workflow from a request only to view data.

## Daily workflow

Intent: collect GitHub, Google News, and YouTube data, execute the ML marketing
pipeline, and show the resulting campaigns. Examples of user requests include
"Run the Daily", "Ejecuta el daily", and "Obtén datos de GitHub, Google News y
YouTube, ejecuta el pipeline de ML y muestra las campañas".

Prerequisites: the server needs a working database and source search
configuration. Fetch tools load that configuration automatically; they accept
no search terms, dates, or other arguments. YouTube requires YOUTUBE_API_KEY;
the pipeline requires GEMINI_API_KEY. GITHUB_TOKEN is optional. These are server
settings, not tool arguments. There is no MCP tool to update search settings.

Execute these calls in order. Each entry is a tool name and its JSON arguments:

```json
[
  {"name": "fetch_github_repos", "arguments": {}},
  {"name": "fetch_google_news_articles", "arguments": {}},
  {"name": "fetch_youtube_videos", "arguments": {}},
  {
    "name": "run_marketing_pipeline",
    "arguments": {
      "limit_per_source": 50,
      "n_clusters": 5,
      "campaign_type": "linkedin_post",
      "translate_non_english": true
    }
  },
  {"name": "get_marketing_campaigns", "arguments": {"limit": 20, "status": "draft"}}
]
```

1. Fetch and save data from all three sources. Record the reported count and
   outcome for each source. The three fetches are independent and may run in
   parallel, but all must finish before the pipeline starts.
2. Run the pipeline once after fetching. It reads pending stored data, cleans
   and normalizes it, optionally translates it to English, filters B2B intent,
   clusters topics with local ML, and generates and saves campaigns using
   Gemini. It can include pending data from earlier fetches; it is not restricted
   to today's data or the records just fetched. Generated copy is currently
   requested in Mexican Spanish (es-MX) and campaigns start with status `draft`.
3. Retain the pipeline's `campaigns` and `stats`, then query saved draft campaigns.
   `get_marketing_campaigns` returns the most recent campaigns across runs, not
   only this Daily. Match by the IDs returned in the pipeline's `campaigns` to
   identify the new results. Its limit can omit some new results; use the pipeline
   response to display those too. Label older campaigns as existing campaigns.
4. Show the source counts, pipeline statistics, and generated campaigns to the
   user. Include each campaign's id, topic_label, campaign_type, hook, body, cta,
   hashtags, and status. Showing campaigns does not publish or approve them;
   this server exposes no tool for either action.

## Arguments and results

- `fetch_github_repos`, `fetch_google_news_articles`, `fetch_youtube_videos`:
  arguments `{}`. Return a text summary of the number fetched and saved via
  UPSERT. The count is not necessarily a count of newly inserted records.
- `get_recent_github_repos`, `get_recent_news_articles`,
  `get_recent_youtube_videos`: `limit` (integer, default 10), `offset` (integer,
  default 0). Return text summaries of saved records. Use a positive limit and
  a non-negative offset; advance offset to read more records.
- `run_marketing_pipeline`: `limit_per_source` (integer, default 50),
  `n_clusters` (integer, default 5), `campaign_type` (default `linkedin_post`;
  supported values `linkedin_post`, `twitter_thread`, `email_newsletter`),
  `translate_non_english` (boolean, default true). Use positive limits and cluster
  counts. Respect the user's requested format and overrides; otherwise use the
  defaults above. The number of campaigns is not guaranteed to equal n_clusters.
  Returns `campaigns` and `stats` with clusters_found, items_processed,
  items_after_filter, total_fetched, discarded_empty_body, translated,
  passed_cleaning, and by_source. Here total_fetched describes data read by the
  pipeline, not the sum of the preceding external fetch counts. The pipeline
  writes normalized data, clusters, campaigns, and processing flags.
- `get_marketing_campaigns`: `limit` (integer, default 20), `status` (optional;
  `draft`, `approved`, `published`; omit or pass null for all statuses). Returns
  a list, most recent first, with campaign fields and created_at. There is no
  date, run ID, or offset argument.

## Errors, empty results, and retries

- Inspect each tool result before the next dependent step. A tool exception or
  MCP error must be reported. The pipeline can also return an `error` field
  (for example, missing GEMINI_API_KEY); treat it as a failed run even when the
  MCP call itself succeeds.
- If a fetch fails, report the source and the incomplete Daily. Other independent
  fetches can finish. Continue with partial or previously stored data only if
  that matches the user's request; otherwise ask whether to continue.
- A fetch count of zero does not prove that no external content exists: source
  integrations may catch upstream errors and return an empty result. State what
  was returned without inventing a cause. Pending stored data may still produce
  campaigns even when the current fetches return zero.
- If `campaigns` is empty, report that this run generated no campaigns and show
  the available stats. There may be no pending items or no items passing the
  filters. Existing campaigns returned by the reader are not new Daily results.
- Do not automatically repeat the full Daily or pipeline after an error or a
  timeout: writes may already have occurred. Report the failure and inspect
  saved campaigns as needed before deciding on a retry. Do not claim success
  for a failed pipeline just because older campaigns exist.
"""


@mcp.tool(
    name="get-documentation-mcp",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def get_documentation_mcp() -> str:
    """Get the MCP guide for choosing tools by user intent and ordering calls.

    Call this first when planning a workflow, especially Daily: fetch GitHub,
    Google News, and YouTube data, run the ML pipeline, then show campaigns.
    Includes exact tool names, arguments, defaults, prerequisites, and error
    handling. Takes no arguments and returns documentation without executing
    tools or accessing the database or external services.
    """
    return MCP_DOCUMENTATION
