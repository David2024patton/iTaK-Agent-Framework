"""OpenCLIP embedding providers."""

from itak.rag.embeddings.providers.openclip.openclip_provider import (
    OpenCLIPProvider,
)
from itak.rag.embeddings.providers.openclip.types import (
    OpenCLIPProviderConfig,
    OpenCLIPProviderSpec,
)


__all__ = [
    "OpenCLIPProvider",
    "OpenCLIPProviderConfig",
    "OpenCLIPProviderSpec",
]
