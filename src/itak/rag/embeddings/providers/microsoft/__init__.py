"""Microsoft embedding providers."""

from itak.rag.embeddings.providers.microsoft.azure import (
    AzureProvider,
)
from itak.rag.embeddings.providers.microsoft.types import (
    AzureProviderConfig,
    AzureProviderSpec,
)


__all__ = [
    "AzureProvider",
    "AzureProviderConfig",
    "AzureProviderSpec",
]
