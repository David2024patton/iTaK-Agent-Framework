"""ONNX embedding providers."""

from itak.rag.embeddings.providers.onnx.onnx_provider import ONNXProvider
from itak.rag.embeddings.providers.onnx.types import (
    ONNXProviderConfig,
    ONNXProviderSpec,
)


__all__ = [
    "ONNXProvider",
    "ONNXProviderConfig",
    "ONNXProviderSpec",
]
