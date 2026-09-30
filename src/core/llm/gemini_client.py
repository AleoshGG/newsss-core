import asyncio

from google import genai
from google.genai import types

from .llm_client import LLMClient


class GeminiLLMClient(LLMClient):
    """
    Google Gemini LLM client using the current google-genai SDK.
    Uses gemini-2.0-flash by default for a good balance of speed and quality.
    Swap model_name for 'gemini-1.5-pro' for higher quality at higher latency/cost.

    All API calls are synchronous in the google-genai SDK, so we wrap them
    in asyncio.to_thread to avoid blocking FastAPI's async event loop — same pattern
    used by YouTubeTranscriptApi in the existing fetcher.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name

    async def generate(self, prompt: str, *, temperature: float = 0.7) -> str:
        """Send a prompt to Gemini and return the text response."""
        config = types.GenerateContentConfig(temperature=temperature)

        def _call() -> str:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=config,
            )
            return response.text

        return await asyncio.to_thread(_call)

    async def translate_to_english(self, text: str) -> str:
        """
        Translate text to English using Gemini.
        Uses low temperature for deterministic, accurate translation.
        Truncates input to 3000 chars to limit token usage.
        """
        prompt = (
            "Translate the following text to English. "
            "Return ONLY the translated text — no explanations, no introductions.\n\n"
            f"{text[:3000]}"
        )
        return await self.generate(prompt, temperature=0.1)
