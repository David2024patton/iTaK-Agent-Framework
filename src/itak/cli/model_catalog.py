# Model Catalog for iTaK Framework
# Organized by category and family with descriptions and metadata
# Order: Core use cases first, specialized/enterprise at bottom

OLLAMA_MODEL_CATALOG = {
    # ============== CORE CATEGORIES (Most Used) ==============
    
    "[REASONING] Deep Thinking Models": {
        "description": "Models that think step-by-step to solve complex problems",
        "families": {
            "DeepSeek R1": {
                "desc": "Open reasoning models rivaling OpenAI o3 and Google Gemini 2.5 Pro",
                "models": {
                    "deepseek-r1:1.5b": {"size": "1.1GB", "ctx": "128K", "desc": "Fast reasoning, lightweight"},
                    "deepseek-r1:7b": {"size": "4.7GB", "ctx": "128K", "desc": "Balanced reasoning power"},
                    "deepseek-r1:8b": {"size": "5.2GB", "ctx": "128K", "desc": "Enhanced reasoning (default)"},
                    "deepseek-r1:14b": {"size": "9.0GB", "ctx": "128K", "desc": "Strong reasoning, mid-size"},
                    "deepseek-r1:32b": {"size": "20GB", "ctx": "128K", "desc": "Very deep reasoning"},
                }
            },
            "Qwen3": {
                "desc": "Alibaba's latest LLMs - fast and smart for everyday tasks",
                "models": {
                    "qwen3:0.6b": {"size": "523MB", "ctx": "40K", "desc": "Ultra-lightweight, for phones"},
                    "qwen3:1.7b": {"size": "1.4GB", "ctx": "40K", "desc": "Light and fast general purpose"},
                    "qwen3:4b": {"size": "2.5GB", "ctx": "256K", "desc": "Efficient general purpose"},
                    "qwen3:8b": {"size": "5.2GB", "ctx": "40K", "desc": "Balanced performance (default)"},
                    "qwen3:14b": {"size": "9.3GB", "ctx": "40K", "desc": "High capability general"},
                    "qwen3:30b": {"size": "19GB", "ctx": "256K", "desc": "Very high capability"},
                }
            },
            "Cogito": {
                "desc": "Hybrid reasoning by Deep Cogito - beats LLaMA, DeepSeek, Qwen at same size",
                "models": {
                    "cogito:3b": {"size": "2.2GB", "ctx": "128K", "desc": "Thinking model, compact"},
                    "cogito:8b": {"size": "4.9GB", "ctx": "128K", "desc": "Thinking model, balanced"},
                    "cogito:14b": {"size": "9.0GB", "ctx": "128K", "desc": "Thinking model, powerful"},
                }
            },
        }
    },
    "[CODING] Development Models": {
        "description": "Models specialized for writing, fixing, and understanding code",
        "families": {
            "Qwen2.5 Coder": {
                "desc": "State-of-the-art open-source code generation, reasoning, and fixing",
                "models": {
                    "qwen2.5-coder:0.5b": {"size": "398MB", "ctx": "32K", "desc": "Ultra-fast code completion"},
                    "qwen2.5-coder:1.5b": {"size": "986MB", "ctx": "32K", "desc": "Quick code assistance"},
                    "qwen2.5-coder:3b": {"size": "1.9GB", "ctx": "32K", "desc": "Efficient coding"},
                    "qwen2.5-coder:7b": {"size": "4.7GB", "ctx": "32K", "desc": "Strong coding (default)"},
                    "qwen2.5-coder:14b": {"size": "9.0GB", "ctx": "32K", "desc": "Advanced code generation"},
                    "qwen2.5-coder:32b": {"size": "20GB", "ctx": "32K", "desc": "Expert-level coding"},
                }
            },
            "Magicoder": {
                "desc": "Trained on real open-source code - produces realistic, practical code",
                "models": {
                    "magicoder:7b": {"size": "4.1GB", "ctx": "16K", "desc": "OSS-trained, low-bias code"},
                }
            },
            "Yi Coder": {
                "desc": "State-of-the-art coding with fewer than 10B parameters",
                "models": {
                    "yi-coder:9b": {"size": "5.0GB", "ctx": "128K", "desc": "SOTA code, long context"},
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
                "desc": "Additional specialized coding models",
                "models": {
                    "mini-coder": {"size": "2.5GB", "ctx": "256K", "desc": "Compact coder, long context"},
                }
            },
        }
    },
    "[AGENTS] Tool-Calling Models": {
        "description": "Models that can use tools, call functions, and work as AI agents",
        "families": {
            "Qwen Cline": {
                "desc": "Optimized for Cline autonomous coding agent workflows",
                "models": {
                    "qwen2.5-coder-cline:7b": {"size": "4.7GB", "ctx": "32K", "desc": "Cline-optimized coding agent"},
                    "qwen2.5-coder-cline:14b": {"size": "9.0GB", "ctx": "32K", "desc": "Advanced Cline agent"},
                }
            },
            "Yi Coder Cline": {
                "desc": "Yi-based models tuned for autonomous coding agents",
                "models": {
                    "yi-coder-cline:9b": {"size": "5.0GB", "ctx": "128K", "desc": "Yi-based Cline agent"},
                }
            },
            "Hermes": {
                "desc": "Nous Research flagship - great for chat and calling external tools",
                "models": {
                    "hermes3:3b": {"size": "2.0GB", "ctx": "128K", "desc": "Chat & function calling"},
                    "hermes3:8b": {"size": "4.7GB", "ctx": "128K", "desc": "Strong function calling"},
                }
            },
        }
    },
    "[VISION] Multimodal Models": {
        "description": "Models that can see and understand images along with text",
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
    "[LIGHTWEIGHT] Phone & Tablet Models": {
        "description": "Small models that run on phones, tablets, and low-power devices",
        "families": {
            "SmolLM2": {
                "desc": "Compact models (135M-1.7B) that can run directly on your phone",
                "models": {
                    "smollm2:135m": {"size": "271MB", "ctx": "8K", "desc": "Tiny, runs on phone"},
                    "smollm2:360m": {"size": "726MB", "ctx": "8K", "desc": "Small, fast on phone"},
                    "smollm2:1.7b": {"size": "1.8GB", "ctx": "8K", "desc": "Compact balanced"},
                }
            },
        }
    },
    
    # ============== UNCENSORED MODELS ==============
    
    "[UNCENSORED] Abliterated Models": {
        "description": "Safety filters mathematically removed - won't refuse requests (use responsibly)",
        "families": {
            "Qwen Abliterated": {
                "desc": "Qwen coder with refusal behavior surgically removed via abliteration",
                "models": {
                    "qwen2.5-coder-abliterate:0.5b": {"size": "398MB", "ctx": "32K", "desc": "No refusals, ultra-light"},
                    "qwen2.5-coder-abliterate:1.5b": {"size": "1.1GB", "ctx": "32K", "desc": "No refusals, fast"},
                    "qwen2.5-coder-abliterate:3b": {"size": "1.9GB", "ctx": "32K", "desc": "No refusals, efficient"},
                    "qwen2.5-coder-abliterate:7b": {"size": "4.7GB", "ctx": "32K", "desc": "No refusals, balanced"},
                    "qwen2.5-coder-abliterate:14b": {"size": "9.0GB", "ctx": "32K", "desc": "No refusals, powerful"},
                }
            },
            "DeepHermes Abliterated": {
                "desc": "Nous Research DeepHermes with reasoning + refusal behavior removed",
                "models": {
                    "huihui_ai/deephermes3-abliterated:8b": {"size": "4.9GB", "ctx": "128K", "desc": "Reasoning, no refusals"},
                }
            },
        }
    },
    
    # ============== SPECIALIZED CATEGORIES (Less Common) ==============
    
    "[ENTERPRISE] Business Models": {
        "description": "Enterprise-grade models from major companies (IBM, NVIDIA, Cohere)",
        "families": {
            "IBM Granite MoE": {
                "desc": "Mixture-of-Experts: uses multiple small expert networks for efficiency",
                "models": {
                    "granite3.1-moe:1b": {"size": "1.4GB", "ctx": "128K", "desc": "MoE = fast + efficient"},
                    "granite3.1-moe:3b": {"size": "2.0GB", "ctx": "128K", "desc": "MoE = fast + efficient"},
                    "granite3-moe:1b": {"size": "822MB", "ctx": "4K", "desc": "MoE compact"},
                    "granite3-moe:3b": {"size": "2.1GB", "ctx": "4K", "desc": "MoE efficient"},
                }
            },
            "IBM Granite Dense": {
                "desc": "Dense = all neurons active (more accurate but slower than MoE)",
                "models": {
                    "granite3.3:2b": {"size": "1.5GB", "ctx": "128K", "desc": "Dense = more accurate"},
                    "granite3.3:8b": {"size": "4.9GB", "ctx": "128K", "desc": "Dense = more accurate"},
                    "granite3-dense:2b": {"size": "1.6GB", "ctx": "4K", "desc": "Dense architecture"},
                    "granite3-dense:8b": {"size": "4.9GB", "ctx": "4K", "desc": "Dense, strong"},
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
                "desc": "Mistral AI Mixture-of-Experts - 8 expert networks working together",
                "models": {
                    "mixtral:8x7b": {"size": "26GB", "ctx": "32K", "desc": "8x7B experts, powerful"},
                }
            },
            "Command R": {
                "desc": "Cohere Labs enterprise LLMs - RAG with citations, tool use, 10+ languages",
                "models": {
                    "c4ai-command-r7b:7b": {"size": "5.1GB", "ctx": "128K", "desc": "RAG + agentic + multilingual"},
                    "command-r-plus:latest": {"size": "63GB", "ctx": "128K", "desc": "Most powerful, enterprise-grade"},
                }
            },
            "Aya Expanse": {
                "desc": "Cohere multilingual model supporting 23+ languages",
                "models": {
                    "aya-expanse:8b": {"size": "5.1GB", "ctx": "8K", "desc": "Multilingual, 23+ languages"},
                }
            },
            "Nemotron": {
                "desc": "NVIDIA small model optimized for roleplay, RAG, and function calling",
                "models": {
                    "nemotron-mini:4b": {"size": "2.7GB", "ctx": "4K", "desc": "NVIDIA efficient model"},
                }
            },
            "Essential AI": {
                "desc": "Dense model trained from scratch, optimized for code and STEM",
                "models": {
                    "rnj-1:8b": {"size": "5.1GB", "ctx": "32K", "desc": "Code + STEM optimized"},
                }
            },
            "Township Small Business": {
                "desc": "Social media marketing chatbot for small businesses - generates posts, hashtags, visuals",
                "models": {
                    "puseletso55/township_smal_business:latest": {"size": "4.1GB", "ctx": "8K", "desc": "SMB social media marketing"},
                }
            },
        }
    },
    "[FINANCE] Trading & Economics Models": {
        "description": "Models for finance, trading, investing, risk analysis, and market psychology",
        "families": {
            "Fin-R1": {
                "desc": "Financial reasoning LLM for insurance, trust, securities, and banking",
                "models": {
                    "mychen76/Fin-R1:Q6": {"size": "5.9GB", "ctx": "8K", "desc": "Financial reasoning, Q6"},
                }
            },
            "Plutus": {
                "desc": "Trained on 394 books: finance, trading, psychology, social engineering",
                "models": {
                    "0xroyce/plutus:latest": {"size": "4.9GB", "ctx": "128K", "desc": "Finance + psychology + trading"},
                }
            },
        }
    },
    "[LEGAL] Law Models": {
        "description": "Models trained on legal texts - for legal research and drafting assistance",
        "families": {
            "Law Model": {
                "desc": "Fine-tuned on Mistral 7B for legal and law - acts as a legal virtual assistant",
                "models": {
                    "initium/law_model:Q2_K": {"size": "2.7GB", "ctx": "8K", "desc": "Legal assistant, smallest"},
                    "initium/law_model:Q3_K_M": {"size": "3.3GB", "ctx": "8K", "desc": "Legal assistant, balanced"},
                    "initium/law_model:Q5_0": {"size": "4.4GB", "ctx": "8K", "desc": "Legal assistant, quality"},
                    "initium/law_model:Q8_0": {"size": "7.2GB", "ctx": "8K", "desc": "Legal assistant, best quality"},
                }
            },
        }
    },
    "[MEDICAL] Healthcare Models": {
        "description": "Models trained on medical literature - for healthcare research only",
        "families": {
            "Meditron": {
                "desc": "Open-source medical LLM adapted from Llama 2 for healthcare",
                "models": {
                    "meditron:7b": {"size": "4.1GB", "ctx": "4K", "desc": "Medical knowledge, research"},
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
    "medical": "meditron:7b",
    "legal": "initium/law_model:Q5_0",
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
