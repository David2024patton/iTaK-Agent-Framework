"""HuggingFace embedding providers."""

from itak.rag.embeddings.providers.huggingface.huggingface_provider import (
    HuggingFaceProvider,
)
from itak.rag.embeddings.providers.huggingface.types import (
    HuggingFaceProviderConfig,
    HuggingFaceProviderSpec,
)


__all__ = [
    "HuggingFaceProvider",
    "HuggingFaceProviderConfig",
    "HuggingFaceProviderSpec",
]
