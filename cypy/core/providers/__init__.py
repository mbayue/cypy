from cypy.core.providers.base import LLMProvider
from cypy.core.providers.gemini import GeminiProvider
from cypy.core.providers.openrouter import OpenRouterProvider
from cypy.core.providers.openai_provider import OpenAIProvider

PROVIDER_MAP = {
    "gemini": GeminiProvider,
    "openrouter": OpenRouterProvider,
    "openai": OpenAIProvider,
}


def create_provider(provider_name, api_key, model_name):
    """Factory function to create the appropriate LLM provider~ ♪"""
    provider_cls = PROVIDER_MAP.get(provider_name.lower())
    if provider_cls is None:
        raise ValueError(
            f"Unknown provider '{provider_name}'. "
            f"Available: {', '.join(PROVIDER_MAP.keys())}"
        )
    return provider_cls(api_key=api_key, model_name=model_name)
