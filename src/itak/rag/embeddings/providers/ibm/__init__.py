"""IBM embedding providers."""

from itak.rag.embeddings.providers.ibm.types import (
    WatsonXProviderConfig,
    WatsonXProviderSpec,
)
from itak.rag.embeddings.providers.ibm.watsonx import (
    WatsonXProvider,
)


__all__ = [
    "WatsonXProvider",
    "WatsonXProviderConfig",
    "WatsonXProviderSpec",
]
