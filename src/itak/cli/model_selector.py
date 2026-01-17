# Model Selector CLI for iTaK Framework
# Beautiful categorized display with multi-download support

import click
import subprocess
import requests
from .model_catalog import OLLAMA_MODEL_CATALOG, RECOMMENDED_MODELS, get_model_info

def display_model_menu():
    """Display beautiful categorized model menu"""
    click.secho("\n" + "="*70, fg="cyan")
    click.secho("🤖 iTaK MODEL CATALOG", fg="cyan", bold=True)
    click.secho("="*70, fg="cyan")
    
    model_index = 1
    model_map = {}  # Maps index to model name
    
    for category_name, category_data in OLLAMA_MODEL_CATALOG.items():
        # Category header
        click.secho(f"\n{category_name}", fg="yellow", bold=True)
        click.secho(f"   {category_data['description']}", fg="white", dim=True)
        click.secho("-" * 68, fg="white", dim=True)
        
        for model_name, model_info in category_data["models"].items():
            model_map[model_index] = model_name
            
            # Format: [index] model_name (size) - description
            size_str = f"[{model_info['size']}]".ljust(10)
            ctx_str = f"{model_info['ctx']}".ljust(5)
            
            # Check if it's a recommended model
            is_recommended = model_name in RECOMMENDED_MODELS.values()
            star = "⭐" if is_recommended else "  "
            
            click.secho(f"   {star} ", nl=False)
            click.secho(f"{str(model_index).rjust(2)}. ", fg="green", nl=False)
            click.secho(f"{model_name.ljust(30)}", fg="bright_white", bold=True, nl=False)
            click.secho(f" {size_str}", fg="cyan", nl=False)
            click.secho(f" {ctx_str}", fg="magenta", nl=False)
            click.secho(f" {model_info['desc']}", fg="white", dim=True)
            
            model_index += 1
    
    click.secho("\n" + "="*70, fg="cyan")
    click.secho("⭐ = Recommended for iTaK agents", fg="yellow")
    click.secho("="*70 + "\n", fg="cyan")
    
    return model_map

def select_models_interactive():
    """
    Interactive model selection with multi-download support.
    Returns list of selected model names.
    """
    model_map = display_model_menu()
    total_models = len(model_map)
    
    click.secho("📥 Select models to download:", fg="green", bold=True)
    click.secho("   • Enter numbers separated by commas (e.g., 1,5,12)", fg="white")
    click.secho("   • Enter 'r' for recommended set", fg="white")
    click.secho("   • Enter 'a' for all models (warning: very large!)", fg="white")
    click.secho("   • Enter 'q' to skip\n", fg="white")
    
    selection = click.prompt("Your choice", type=str, default="r")
    
    if selection.lower() == 'q':
        return []
    
    if selection.lower() == 'r':
        # Return recommended models
        return list(RECOMMENDED_MODELS.values())
    
    if selection.lower() == 'a':
        if click.confirm("⚠️  This will download ALL models (~200GB+). Continue?", default=False):
            return list(model_map.values())
        return []
    
    # Parse comma-separated numbers
    try:
        indices = [int(x.strip()) for x in selection.split(",")]
        selected = []
        for idx in indices:
            if 1 <= idx <= total_models:
                selected.append(model_map[idx])
            else:
                click.secho(f"⚠️  Invalid number: {idx} (must be 1-{total_models})", fg="yellow")
        return selected
    except ValueError:
        click.secho("❌ Invalid input. Please enter numbers separated by commas.", fg="red")
        return []

def download_models(model_names, show_progress=True):
    """
    Download multiple models from Ollama.
    Returns dict of {model_name: success_bool}
    """
    results = {}
    total = len(model_names)
    
    if total == 0:
        click.secho("ℹ️  No models selected.", fg="yellow")
        return results
    
    click.secho(f"\n📥 Downloading {total} model(s)...\n", fg="cyan", bold=True)
    
    for i, model_name in enumerate(model_names, 1):
        info = get_model_info(model_name)
        size_str = info['size'] if info else "?"
        
        click.secho(f"[{i}/{total}] ", fg="green", nl=False)
        click.secho(f"Pulling {model_name} ", fg="bright_white", bold=True, nl=False)
        click.secho(f"({size_str})...", fg="cyan")
        
        try:
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=not show_progress,
                text=True
            )
            
            if result.returncode == 0:
                click.secho(f"   ✅ {model_name} downloaded successfully!", fg="green")
                results[model_name] = True
            else:
                click.secho(f"   ❌ Failed to download {model_name}", fg="red")
                results[model_name] = False
        except Exception as e:
            click.secho(f"   ❌ Error: {e}", fg="red")
            results[model_name] = False
    
    # Summary
    success_count = sum(1 for v in results.values() if v)
    click.secho(f"\n{'='*70}", fg="cyan")
    click.secho(f"📊 Download Summary: {success_count}/{total} successful", 
                fg="green" if success_count == total else "yellow", bold=True)
    click.secho(f"{'='*70}\n", fg="cyan")
    
    return results

def check_and_pull_model(model_name):
    """
    Check if a model is available locally, pull if not.
    Used by self-healing auto-run.
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get("models", [])
        model_names = [m.get("name", "") for m in models]
        
        # Check various name formats
        if model_name in model_names:
            return True
        if f"{model_name}:latest" in model_names:
            return True
        if any(model_name in m for m in model_names):
            return True
        
        # Model not found, pull it
        info = get_model_info(model_name)
        size_str = info['size'] if info else "unknown size"
        
        click.secho(f"⚠️  Model '{model_name}' not found locally.", fg="yellow")
        click.secho(f"   Downloading {model_name} ({size_str})...", fg="yellow")
        click.secho("   (This may take a few minutes on first run)", fg="white", dim=True)
        
        result = subprocess.run(["ollama", "pull", model_name], capture_output=False)
        
        if result.returncode == 0:
            click.secho(f"✅ Model '{model_name}' downloaded successfully!", fg="green")
            return True
        else:
            click.secho(f"❌ Failed to download '{model_name}'", fg="red")
            return False
            
    except Exception as e:
        click.secho(f"⚠️  Could not check models: {e}", fg="yellow")
        return False

def get_quick_model_selection():
    """Quick model selection by category for crew creation"""
    click.secho("\n🎯 Quick Model Selection:", fg="cyan", bold=True)
    click.secho("="*50, fg="cyan")
    
    options = [
        ("1", "qwen2.5-coder:7b", "💻 Best for coding (4.7GB)"),
        ("2", "deepseek-r1:8b", "🧠 Best for reasoning (5.2GB)"),
        ("3", "qwen3:8b", "⚡ Best general purpose (5.2GB)"),
        ("4", "qwen3-vl:8b", "👁️ Best for vision (6.1GB)"),
        ("5", "qwen2.5-coder-cline:7b", "🤖 Best for agents (4.7GB)"),
        ("6", "smollm2:1.7b", "🪶 Lightweight (1.8GB)"),
        ("c", None, "📋 Show full catalog"),
    ]
    
    for opt, model, desc in options:
        click.secho(f"  {opt}. ", fg="green", nl=False)
        click.secho(desc, fg="white")
    
    choice = click.prompt("\nSelect", type=str, default="1")
    
    if choice == 'c':
        selected = select_models_interactive()
        return selected[0] if selected else "qwen2.5-coder:7b"
    
    for opt, model, _ in options:
        if choice == opt and model:
            return model
    
    return "qwen2.5-coder:7b"  # Default
