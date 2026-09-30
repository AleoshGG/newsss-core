from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract interface for LLM providers.
    Implement this to add new providers (Gemini, OpenAI, Anthropic, Ollama, etc.)
    without changing any business logic.
    """

    @abstractmethod
    async def generate(self, prompt: str, *, temperature: float = 0.7) -> str:
        """Send a prompt and return the generated text response."""
        ...

    @abstractmethod
    async def translate_to_english(self, text: str) -> str:
        """
        Translate arbitrary text to English.
        Returns the original text unchanged if it is already in English.
        """
        ...
