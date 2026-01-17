# Model Catalog for iTaK Framework
# Organized by category and family with descriptions and metadata

OLLAMA_MODEL_CATALOG = {
    "[REASONING] Deep Thinking Models": {
        "description": "Deep thinking models for complex reasoning tasks",
        "families": {
            "DeepSeek R1": {
                "desc": "Open reasoning models with performance approaching O3 and Gemini 2.5 Pro",
                "models": {
                    "deepseek-r1:1.5b": {"size": "1.1GB", "ctx": "128K", "desc": "Fast reasoning, lightweight"},
                    "deepseek-r1:7b": {"size": "4.7GB", "ctx": "128K", "desc": "Balanced reasoning power"},
                    "deepseek-r1:8b": {"size": "5.2GB", "ctx": "128K", "desc": "Enhanced reasoning (default)"},
                    "deepseek-r1:14b": {"size": "9.0GB", "ctx": "128K", "desc": "Strong reasoning, mid-size"},
                    "deepseek-r1:32b": {"size": "20GB", "ctx": "128K", "desc": "Very deep reasoning"},
                }
            },
            "Qwen3": {
                "desc": "Latest generation Qwen LLMs with dense and mixture-of-experts variants",
                "models": {
                    "qwen3:0.6b": {"size": "523MB", "ctx": "40K", "desc": "Ultra-lightweight, edge devices"},
                    "qwen3:1.7b": {"size": "1.4GB", "ctx": "40K", "desc": "Light and fast general purpose"},
                    "qwen3:4b": {"size": "2.5GB", "ctx": "256K", "desc": "Efficient general purpose"},
                    "qwen3:8b": {"size": "5.2GB", "ctx": "40K", "desc": "Balanced performance (default)"},
                    "qwen3:14b": {"size": "9.3GB", "ctx": "40K", "desc": "High capability general"},
                    "qwen3:30b": {"size": "19GB", "ctx": "256K", "desc": "Very high capability"},
                }
            },
            "Cogito": {
                "desc": "Hybrid reasoning models by Deep Cogito, outperforming LLaMA/DeepSeek/Qwen",
                "models": {
                    "cogito:3b": {"size": "2.2GB", "ctx": "128K", "desc": "Thinking model, compact"},
                    "cogito:8b": {"size": "4.9GB", "ctx": "128K", "desc": "Thinking model, balanced"},
                    "cogito:14b": {"size": "9.0GB", "ctx": "128K", "desc": "Thinking model, powerful"},
                }
            },
        }
    },
    "[CODING] Development Models": {
        "description": "Specialized models for code generation and development",
        "families": {
            "Qwen2.5 Coder": {
                "desc": "Code-specific Qwen with SOTA code generation, reasoning, and fixing",
                "models": {
                    "qwen2.5-coder:0.5b": {"size": "398MB", "ctx": "32K", "desc": "Ultra-fast code completion"},
                    "qwen2.5-coder:1.5b": {"size": "986MB", "ctx": "32K", "desc": "Quick code assistance"},
                    "qwen2.5-coder:3b": {"size": "1.9GB", "ctx": "32K", "desc": "Efficient coding"},
                    "qwen2.5-coder:7b": {"size": "4.7GB", "ctx": "32K", "desc": "Strong coding (default)"},
                    "qwen2.5-coder:14b": {"size": "9.0GB", "ctx": "32K", "desc": "Advanced code generation"},
                    "qwen2.5-coder:32b": {"size": "20GB", "ctx": "32K", "desc": "Expert-level coding"},
                }
            },
            "DeepSeek Coder Tools": {
                "desc": "Modified for autonomous coding agents like Cline with tool support",
                "models": {
                    "deepseek-r1-coder-tools:1.5b": {"size": "3.6GB", "ctx": "128K", "desc": "Reasoning + code + tools"},
                    "deepseek-r1-coder-tools:7b": {"size": "15GB", "ctx": "128K", "desc": "Strong coding with tools"},
                    "deepseek-r1-coder-tools:8b": {"size": "16GB", "ctx": "128K", "desc": "Enhanced tools support"},
                    "deepseek-r1-coder-tools:14b": {"size": "30GB", "ctx": "128K", "desc": "Professional tools coding"},
                }
            },
            "Other Coders": {
                "desc": "Alternative coding models",
                "models": {
                    "mini-coder": {"size": "2.5GB", "ctx": "256K", "desc": "Compact coder, long context"},
                }
            },
        }
    },
    "[AGENTS] Tool-Calling Models": {
        "description": "Models optimized for AI agents and tool use",
        "families": {
            "Qwen Cline": {
                "desc": "Optimized for Cline autonomous coding agent workflows",
                "models": {
                    "qwen2.5-coder-cline:7b": {"size": "4.7GB", "ctx": "32K", "desc": "Cline-optimized coding agent"},
                    "qwen2.5-coder-cline:14b": {"size": "9.0GB", "ctx": "32K", "desc": "Advanced Cline agent"},
                }
            },
            "Qwen Abliterate": {
                "desc": "Uncensored Qwen variants with removed safety filters",
                "models": {
                    "qwen2.5-coder-abliterate:0.5b": {"size": "398MB", "ctx": "32K", "desc": "Uncensored, ultra-light"},
                    "qwen2.5-coder-abliterate:1.5b": {"size": "1.1GB", "ctx": "32K", "desc": "Uncensored, fast"},
                    "qwen2.5-coder-abliterate:3b": {"size": "1.9GB", "ctx": "32K", "desc": "Uncensored, efficient"},
                    "qwen2.5-coder-abliterate:7b": {"size": "4.7GB", "ctx": "32K", "desc": "Uncensored, balanced"},
                    "qwen2.5-coder-abliterate:14b": {"size": "9.0GB", "ctx": "32K", "desc": "Uncensored, powerful"},
                }
            },
            "Yi Coder": {
                "desc": "Yi-based models optimized for coding agents",
                "models": {
                    "yi-coder-cline:9b": {"size": "5.0GB", "ctx": "128K", "desc": "Yi-based Cline agent"},
                }
            },
            "Hermes": {
                "desc": "Nous Research flagship LLM with strong function calling",
                "models": {
                    "hermes3:3b": {"size": "2.0GB", "ctx": "128K", "desc": "Chat & function calling"},
                    "hermes3:8b": {"size": "4.7GB", "ctx": "128K", "desc": "Strong function calling"},
                }
            },
        }
    },
    "[VISION] Multimodal Models": {
        "description": "Models that understand images and text",
        "families": {
            "Qwen3 VL": {
                "desc": "Most powerful vision-language model in Qwen family",
                "models": {
                    "qwen3-vl:2b": {"size": "1.9GB", "ctx": "256K", "desc": "Fast vision, lightweight"},
                    "qwen3-vl:4b": {"size": "3.3GB", "ctx": "256K", "desc": "Efficient vision analysis"},
                    "qwen3-vl:8b": {"size": "6.1GB", "ctx": "256K", "desc": "Balanced vision (default)"},
                    "qwen3-vl:30b": {"size": "20GB", "ctx": "256K", "desc": "High-quality vision"},
                    "qwen3-vl:32b": {"size": "21GB", "ctx": "256K", "desc": "Expert vision analysis"},
                }
            },
            "Granite Vision": {
                "desc": "IBM multimodal models with vision capabilities",
                "models": {
                    "granite3.2-vision:2b": {"size": "2.4GB", "ctx": "16K", "desc": "IBM vision model"},
                }
            },
        }
    },
    "[ENTERPRISE] Specialized Models": {
        "description": "Enterprise-grade and task-specific models",
        "families": {
            "IBM Granite MoE": {
                "desc": "IBM Mixture-of-Experts models for enterprise use",
                "models": {
                    "granite3.1-moe:1b": {"size": "1.4GB", "ctx": "128K", "desc": "IBM MoE, efficient"},
                    "granite3.1-moe:3b": {"size": "2.0GB", "ctx": "128K", "desc": "IBM MoE, balanced"},
                    "granite3-moe:1b": {"size": "822MB", "ctx": "4K", "desc": "IBM MoE compact"},
                    "granite3-moe:3b": {"size": "2.1GB", "ctx": "4K", "desc": "IBM MoE efficient"},
                }
            },
            "IBM Granite Dense": {
                "desc": "IBM 128K context length models with improved reasoning",
                "models": {
                    "granite3.3:2b": {"size": "1.5GB", "ctx": "128K", "desc": "IBM general purpose"},
                    "granite3.3:8b": {"size": "4.9GB", "ctx": "128K", "desc": "IBM strong general"},
                    "granite3-dense:2b": {"size": "1.6GB", "ctx": "4K", "desc": "IBM dense architecture"},
                    "granite3-dense:8b": {"size": "4.9GB", "ctx": "4K", "desc": "IBM dense, strong"},
                }
            },
            "IBM Granite 4": {
                "desc": "Latest IBM Granite models with enhanced capabilities",
                "models": {
                    "granite4:350m": {"size": "708MB", "ctx": "32K", "desc": "Ultra-light IBM"},
                    "granite4:1b": {"size": "3.3GB", "ctx": "128K", "desc": "IBM compact powerful"},
                    "granite4:3b": {"size": "2.1GB", "ctx": "128K", "desc": "IBM efficient"},
                }
            },
            "Mixtral": {
                "desc": "Mistral AI Sparse Mixture-of-Experts, strong math & coding",
                "models": {
                    "mixtral:8x7b": {"size": "26GB", "ctx": "32K", "desc": "Mixture of experts, powerful"},
                }
            },
            "Aya Expanse": {
                "desc": "Cohere multilingual model for 23+ languages",
                "models": {
                    "aya-expanse:8b": {"size": "5.1GB", "ctx": "8K", "desc": "Multilingual, 23+ languages"},
                }
            },
            "Nemotron": {
                "desc": "NVIDIA SLM optimized for roleplay, RAG, and function calling",
                "models": {
                    "nemotron-mini:4b": {"size": "2.7GB", "ctx": "4K", "desc": "NVIDIA efficient model"},
                }
            },
            "Other Enterprise": {
                "desc": "Specialized enterprise models",
                "models": {
                    "command-r7b:7b": {"size": "5.1GB", "ctx": "8K", "desc": "Cohere RAG-optimized"},
                    "rnj-1:8b": {"size": "5.1GB", "ctx": "32K", "desc": "Research model"},
                }
            },
        }
    },
    "[LIGHTWEIGHT] Edge Models": {
        "description": "Ultra-compact models for edge devices and fast inference",
        "families": {
            "SmolLM2": {
                "desc": "Compact language models (135M-1.7B) for on-device deployment",
                "models": {
                    "smollm2:135m": {"size": "271MB", "ctx": "8K", "desc": "Tiny, mobile-ready"},
                    "smollm2:360m": {"size": "726MB", "ctx": "8K", "desc": "Small, fast inference"},
                    "smollm2:1.7b": {"size": "1.8GB", "ctx": "8K", "desc": "Compact balanced"},
                }
            },
        }
    },
}

# Recommended starter models for different use cases
RECOMMENDED_MODELS = {
    "coding": "qwen2.5-coder:7b",
    "reasoning": "deepseek-r1:8b",
    "general": "qwen3:8b",
    "vision": "qwen3-vl:8b",
    "agent": "qwen2.5-coder-cline:7b",
    "lightweight": "smollm2:1.7b",
}

def get_all_model_names():
    """Get flat list of all model names"""
    models = []
    for category in OLLAMA_MODEL_CATALOG.values():
        for family in category.get("families", {}).values():
            models.extend(family["models"].keys())
    return models

def get_model_info(model_name):
    """Get info for a specific model"""
    for category_name, category in OLLAMA_MODEL_CATALOG.items():
        for family_name, family in category.get("families", {}).items():
            if model_name in family["models"]:
                info = family["models"][model_name]
                return {
                    "name": model_name,
                    "category": category_name,
                    "family": family_name,
                    "family_desc": family.get("desc", ""),
                    **info
                }
    return None
