"""Ollama embedding providers."""

from itak.rag.embeddings.providers.ollama.ollama_provider import (
    OllamaProvider,
)
from itak.rag.embeddings.providers.ollama.types import (
    OllamaProviderConfig,
    OllamaProviderSpec,
)


__all__ = [
    "OllamaProvider",
    "OllamaProviderConfig",
    "OllamaProviderSpec",
]
