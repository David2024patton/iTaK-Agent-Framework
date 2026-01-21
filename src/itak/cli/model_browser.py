"""
iTaK Model Browser - Interactive Model Category Selector

Browse and select AI models by category.
"""

import click

# Color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"

# Model catalog organized by category
MODEL_CATALOG = {
    "🎯 General": {
        "description": "All-purpose chat and reasoning",
        "models": [
            {"name": "qwen3:4b", "size": "2.6GB", "desc": "Fast general purpose"},
            {"name": "llama3.2:3b", "size": "2.0GB", "desc": "Meta's latest small"},
            {"name": "gemma3:4b", "size": "3.3GB", "desc": "Google's efficient model"},
            {"name": "phi4:14b", "size": "9.1GB", "desc": "Microsoft reasoning"},
            {"name": "mistral:7b", "size": "4.1GB", "desc": "Strong 7B model"},
        ]
    },
    "👁️ Vision": {
        "description": "Image understanding + text",
        "models": [
            {"name": "qwen3-vl:4b", "size": "3.3GB", "desc": "Vision + language (default)"},
            {"name": "llava:7b", "size": "4.7GB", "desc": "Visual assistant"},
            {"name": "moondream:1.8b", "size": "1.7GB", "desc": "Tiny vision model"},
            {"name": "llava-phi3:3.8b", "size": "2.9GB", "desc": "Fast vision"},
        ]
    },
    "💻 Coding": {
        "description": "Code generation and debugging",
        "models": [
            {"name": "qwen2.5-coder:7b", "size": "4.7GB", "desc": "Best code model"},
            {"name": "codellama:7b", "size": "3.8GB", "desc": "Meta code specialist"},
            {"name": "deepseek-coder:6.7b", "size": "3.8GB", "desc": "Deep code understanding"},
            {"name": "starcoder2:7b", "size": "4.0GB", "desc": "Multi-language coder"},
        ]
    },
    "🧠 Reasoning": {
        "description": "Complex logic and math",
        "models": [
            {"name": "qwq:32b", "size": "20GB", "desc": "Advanced reasoning"},
            {"name": "deepseek-r1:8b", "size": "4.9GB", "desc": "Chain of thought"},
            {"name": "phi4:14b", "size": "9.1GB", "desc": "Strong reasoning"},
        ]
    },
    "⚡ Fast (CPU OK)": {
        "description": "Lightweight models for any hardware",
        "models": [
            {"name": "qwen3:0.6b", "size": "0.5GB", "desc": "Ultra fast"},
            {"name": "gemma3:1b", "size": "0.8GB", "desc": "Tiny but capable"},
            {"name": "tinyllama:1.1b", "size": "0.6GB", "desc": "Very lightweight"},
            {"name": "moondream:1.8b", "size": "1.7GB", "desc": "Fast vision"},
        ]
    },
    "🔧 Specialized": {
        "description": "Domain-specific models",
        "models": [
            {"name": "meditron:7b", "size": "3.9GB", "desc": "Medical knowledge"},
            {"name": "sqlcoder:7b", "size": "4.1GB", "desc": "SQL generation"},
            {"name": "magicoder:7b", "size": "3.8GB", "desc": "Code instruction"},
        ]
    },
}


def show_categories():
    """Show available model categories."""
    print(f"\n{BOLD}Model Categories:{RESET}\n")
    
    categories = list(MODEL_CATALOG.keys())
    for i, cat in enumerate(categories, 1):
        desc = MODEL_CATALOG[cat]["description"]
        count = len(MODEL_CATALOG[cat]["models"])
        print(f"  {GREEN}{i}{RESET}. {cat}")
        print(f"     {DIM}{desc} ({count} models){RESET}")
    
    print(f"\n  {YELLOW}0{RESET}. Back to chat")
    print()
    
    return categories


def show_models_in_category(category_name: str, models: list):
    """Show models within a category."""
    print(f"\n{BOLD}{category_name}{RESET}\n")
    
    for i, model in enumerate(models, 1):
        name = model["name"]
        size = model["size"]
        desc = model["desc"]
        print(f"  {GREEN}{i}{RESET}. {CYAN}{name}{RESET}")
        print(f"     {DIM}{desc} • {size}{RESET}")
    
    print(f"\n  {YELLOW}0{RESET}. Back to categories")
    print()
    
    return models


def browse_models(current_model: str = "ollama/qwen3-vl:4b") -> str:
    """Interactive model browser. Returns selected model name."""
    
    print(f"\n{BOLD}🤖 Model Browser{RESET}")
    print(f"{DIM}Current model: {CYAN}{current_model}{RESET}\n")
    
    while True:
        # Show categories
        categories = show_categories()
        
        try:
            choice = input(f"{GREEN}>{RESET} Select category (1-{len(categories)}, 0 to exit): ").strip()
            
            if choice == "0" or choice.lower() in ["q", "quit", "exit", "back"]:
                print(f"\n{DIM}Keeping model: {current_model}{RESET}")
                return current_model
            
            cat_idx = int(choice) - 1
            if 0 <= cat_idx < len(categories):
                category_name = categories[cat_idx]
                models = MODEL_CATALOG[category_name]["models"]
                
                # Show models in category
                while True:
                    show_models_in_category(category_name, models)
                    
                    model_choice = input(f"{GREEN}>{RESET} Select model (1-{len(models)}, 0 for back): ").strip()
                    
                    if model_choice == "0" or model_choice.lower() == "back":
                        break
                    
                    try:
                        model_idx = int(model_choice) - 1
                        if 0 <= model_idx < len(models):
                            selected = models[model_idx]["name"]
                            # Add ollama/ prefix for proper routing
                            selected = f"ollama/{selected}"
                            print(f"\n{GREEN}✓{RESET} Model set to: {CYAN}{selected}{RESET}\n")
                            return selected
                    except ValueError:
                        print(f"{YELLOW}Please enter a number.{RESET}")
            else:
                print(f"{YELLOW}Please enter 1-{len(categories)}{RESET}")
                
        except ValueError:
            print(f"{YELLOW}Please enter a number.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}Keeping model: {current_model}{RESET}")
            return current_model


if __name__ == "__main__":
    result = browse_models()
    print(f"Selected: {result}")
