"""AWS embedding providers."""

from itak.rag.embeddings.providers.aws.bedrock import BedrockProvider
from itak.rag.embeddings.providers.aws.types import (
    BedrockProviderConfig,
    BedrockProviderSpec,
)


__all__ = [
    "BedrockProvider",
    "BedrockProviderConfig",
    "BedrockProviderSpec",
]
