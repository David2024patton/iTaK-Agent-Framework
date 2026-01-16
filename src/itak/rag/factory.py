"""Factory functions for creating RAG clients from configuration."""

from typing import cast

from itak.rag.config.optional_imports.protocols import (
    ChromaFactoryModule,
    QdrantFactoryModule,
)
from itak.rag.config.types import RagConfigType
from itak.rag.core.base_client import BaseClient
from itak.utilities.import_utils import require


def create_client(config: RagConfigType) -> BaseClient:
    """Create a client from configuration using the appropriate factory.

    Args:
        config: The RAG client configuration.

    Returns:
        The created client instance.

    Raises:
        ValueError: If the configuration provider is not supported.
    """

    if config.provider == "chromadb":
        chromadb_mod = cast(
            ChromaFactoryModule,
            require(
                "iTaK.rag.chromadb.factory",
                purpose="The 'chromadb' provider",
            ),
        )
        return chromadb_mod.create_client(config)

    if config.provider == "qdrant":
        qdrant_mod = cast(
            QdrantFactoryModule,
            require(
                "iTaK.rag.qdrant.factory",
                purpose="The 'qdrant' provider",
            ),
        )
        return qdrant_mod.create_client(config)

    raise ValueError(f"Unsupported provider: {config.provider}")
