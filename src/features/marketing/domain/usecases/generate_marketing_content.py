import json
import uuid
from datetime import datetime, timezone
from typing import Literal

from src.core.llm.llm_client import LLMClient

from ..entities.content_cluster_entity import ContentCluster
from ..entities.marketing_campaign_entity import MarketingCampaign
from ..entities.normalized_item_entity import NormalizedItem


# ---------------------------------------------------------------------------
# Prompt templates — calibrated for B2B / consulting firm audiences
# Audience: CTOs, IT directors, enterprise decision-makers
# ---------------------------------------------------------------------------

_LINKEDIN_PROMPT = """\
You are a senior B2B marketing strategist for a technology consulting firm.
Your audience: CTOs, IT directors, and decision-makers at mid-to-large enterprises.
Tone: Professional, insightful, data-informed. No fluff, no buzzwords.
Goal: Drive meaningful engagement (comments, shares) from B2B decision-makers.
Language: Write your entire response in Spanish as spoken in Mexico (es-MX).

Based on the trending technology cluster below, write a high-performing LinkedIn post.

TOPIC: {topic_label}
KEY THEMES: {keywords}
TRENDING CONTENT REFERENCES:
{sources_summary}

Return a valid JSON object with EXACTLY these keys (no extra keys, no markdown fences):
{{
  "hook": "Primera línea — afirmación audaz o insight sorprendente que detenga el scroll (máx 20 palabras)",
  "body": "3-4 párrafos cortos con insights accionables. Usa saltos de línea. Máx 250 palabras. Sin listas abusivas.",
  "cta": "Una llamada a la acción clara — una pregunta que invite a comentar (máx 20 palabras)",
  "hashtags": ["5", "a", "7", "hashtags", "relevantes", "b2b"]
}}
"""

_TWITTER_PROMPT = """\
You are a B2B tech thought leader writing for founders, VCs, and enterprise buyers on X (Twitter).
Tone: Direct, punchy, data-driven. Each tweet max 280 characters. No filler words.
Goal: Drive retweets and replies from a tech-savvy B2B audience.
Language: Write your entire response in Spanish as spoken in Mexico (es-MX).

Based on this trending cluster, write a 5-tweet thread.

TOPIC: {topic_label}
KEY THEMES: {keywords}
TRENDING CONTENT REFERENCES:
{sources_summary}

Return a valid JSON object with EXACTLY these keys (no extra keys, no markdown fences):
{{
  "hook": "Tweet 1: el gancho que hace que la gente haga clic en 'Ver este hilo' (máx 280 caracteres)",
  "body": ["Tweet 2 insight", "Tweet 3 insight", "Tweet 4 insight"],
  "cta": "Tweet 5: una pregunta o llamada a la acción que genere respuestas (máx 280 caracteres)",
  "hashtags": ["máx", "3", "hashtags"]
}}
"""

_EMAIL_PROMPT = """\
You are writing the weekly technology briefing section for a B2B newsletter.
Subscribers are senior decision-makers (CTOs, VPs of Engineering, founders).
Tone: Executive briefing style — concise, curated, high-signal. No hype.
Goal: Be the most useful email they read this week.
Language: Write your entire response in Spanish as spoken in Mexico (es-MX).

TOPIC: {topic_label}
KEY THEMES: {keywords}
TRENDING CONTENT REFERENCES:
{sources_summary}

Return a valid JSON object with EXACTLY these keys (no extra keys, no markdown fences):
{{
  "hook": "Asunto del correo + texto de vista previa separados por ' | ' (que inviten a abrirlo)",
  "body": "Sección del newsletter: 200-300 palabras. 3 puntos clave con encabezados en markdown en negritas (**Encabezado:**). Alta señal, sin relleno.",
  "cta": "Una acción específica para el lector esta semana (máx 25 palabras)",
  "hashtags": []
}}
"""

CAMPAIGN_PROMPTS: dict[str, str] = {
    "linkedin_post": _LINKEDIN_PROMPT,
    "twitter_thread": _TWITTER_PROMPT,
    "email_newsletter": _EMAIL_PROMPT,
}


# ---------------------------------------------------------------------------
# GenerateMarketingContentUseCase — Stage 4
# ---------------------------------------------------------------------------

class GenerateMarketingContentUseCase:
    """
    Stage 4 of the marketing pipeline.

    Takes a ContentCluster and generates a structured marketing campaign using
    the injected LLMClient (Gemini by default). The prompt is calibrated for
    B2B / consulting firm audiences targeting enterprise decision-makers.

    Supported campaign types: linkedin_post | twitter_thread | email_newsletter
    """

    def __init__(
        self,
        llm: LLMClient,
        campaign_type: Literal["linkedin_post", "twitter_thread", "email_newsletter"] = "linkedin_post",
    ) -> None:
        self._llm = llm
        self._campaign_type = campaign_type

    async def execute(self, cluster: ContentCluster) -> MarketingCampaign:
        """Generates a MarketingCampaign for the given ContentCluster."""
        prompt_template = CAMPAIGN_PROMPTS[self._campaign_type]
        sources_summary = self._format_sources_summary(cluster.representative_items)

        prompt = prompt_template.format(
            topic_label=cluster.topic_label,
            keywords=", ".join(cluster.keywords[:8]),
            sources_summary=sources_summary,
        )

        raw_response = await self._llm.generate(prompt, temperature=0.75)
        parsed = self._parse_llm_response(raw_response)

        return MarketingCampaign(
            id=str(uuid.uuid4()),
            cluster_id=cluster.db_id,
            topic_label=cluster.topic_label,
            campaign_type=self._campaign_type,
            hook=parsed.get("hook"),
            body=parsed.get("body", raw_response),
            cta=parsed.get("cta"),
            hashtags=parsed.get("hashtags", []),
            status="draft",
            created_at=datetime.now(timezone.utc),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_sources_summary(items: list[NormalizedItem]) -> str:
        """
        Formats the top representative items into a compact context block
        for the LLM prompt. Includes source type, title, and a body excerpt.
        """
        lines = []
        for item in items[:5]:
            source_tag = item.source.upper().replace("_", " ")
            excerpt = item.body[:250].replace("\n", " ").strip()
            lines.append(f"[{source_tag}] {item.title}\n  → {excerpt}...")
        return "\n\n".join(lines)

    @staticmethod
    def _parse_llm_response(raw: str) -> dict:
        """
        Attempts to parse the LLM response as JSON.
        Strips markdown code fences (```json ... ```) if present.
        Falls back to a minimal dict with the raw text as body on parse failure.
        """
        text = raw.strip()

        # Strip markdown code fences that some LLMs add despite instructions
        if text.startswith("```"):
            lines = text.splitlines()
            # Remove first line (```json or ```) and last line (```)
            inner = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(inner).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Graceful degradation: treat entire response as the body
            print(f"Warning: LLM response was not valid JSON. Raw: {raw[:200]}")
            return {"hook": None, "body": raw, "cta": None, "hashtags": []}
