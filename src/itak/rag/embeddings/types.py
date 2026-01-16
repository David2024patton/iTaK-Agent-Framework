"""Type definitions for the embeddings module."""

from typing import Any, Literal, TypeAlias

from itak.rag.core.base_embeddings_provider import BaseEmbeddingsProvider
from itak.rag.embeddings.providers.aws.types import BedrockProviderSpec
from itak.rag.embeddings.providers.cohere.types import CohereProviderSpec
from itak.rag.embeddings.providers.custom.types import CustomProviderSpec
from itak.rag.embeddings.providers.google.types import (
    GenerativeAiProviderSpec,
    VertexAIProviderSpec,
)
from itak.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec
from itak.rag.embeddings.providers.ibm.types import (
    WatsonXProviderSpec,
)
from itak.rag.embeddings.providers.instructor.types import InstructorProviderSpec
from itak.rag.embeddings.providers.jina.types import JinaProviderSpec
from itak.rag.embeddings.providers.microsoft.types import AzureProviderSpec
from itak.rag.embeddings.providers.ollama.types import OllamaProviderSpec
from itak.rag.embeddings.providers.onnx.types import ONNXProviderSpec
from itak.rag.embeddings.providers.openai.types import OpenAIProviderSpec
from itak.rag.embeddings.providers.openclip.types import OpenCLIPProviderSpec
from itak.rag.embeddings.providers.roboflow.types import RoboflowProviderSpec
from itak.rag.embeddings.providers.sentence_transformer.types import (
    SentenceTransformerProviderSpec,
)
from itak.rag.embeddings.providers.text2vec.types import Text2VecProviderSpec
from itak.rag.embeddings.providers.voyageai.types import VoyageAIProviderSpec


ProviderSpec: TypeAlias = (
    AzureProviderSpec
    | BedrockProviderSpec
    | CohereProviderSpec
    | CustomProviderSpec
    | GenerativeAiProviderSpec
    | HuggingFaceProviderSpec
    | InstructorProviderSpec
    | JinaProviderSpec
    | OllamaProviderSpec
    | ONNXProviderSpec
    | OpenAIProviderSpec
    | OpenCLIPProviderSpec
    | RoboflowProviderSpec
    | SentenceTransformerProviderSpec
    | Text2VecProviderSpec
    | VertexAIProviderSpec
    | VoyageAIProviderSpec
    | WatsonXProviderSpec
)

AllowedEmbeddingProviders = Literal[
    "azure",
    "amazon-bedrock",
    "cohere",
    "custom",
    "google-generativeai",
    "google-vertex",
    "huggingface",
    "instructor",
    "jina",
    "ollama",
    "onnx",
    "openai",
    "openclip",
    "roboflow",
    "sentence-transformer",
    "text2vec",
    "voyageai",
    "watsonx",
]

EmbedderConfig: TypeAlias = (
    ProviderSpec | BaseEmbeddingsProvider[Any] | type[BaseEmbeddingsProvider[Any]]
)
