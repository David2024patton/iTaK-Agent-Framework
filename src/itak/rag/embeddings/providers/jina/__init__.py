"""Jina embedding providers."""

from itak.rag.embeddings.providers.jina.jina_provider import JinaProvider
from itak.rag.embeddings.providers.jina.types import (
    JinaProviderConfig,
    JinaProviderSpec,
)


__all__ = [
    "JinaProvider",
    "JinaProviderConfig",
    "JinaProviderSpec",
]
