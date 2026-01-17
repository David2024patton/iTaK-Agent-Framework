# Model Selector CLI for iTaK Framework
# Beautiful categorized display with system-aware filtering

import click
import subprocess
import requests
from .model_catalog import OLLAMA_MODEL_CATALOG, RECOMMENDED_MODELS, get_model_info
from .system_detect import (
    get_system_specs, 
    get_model_compatibility, 
    format_specs_summary,
    parse_size_to_gb,
    get_recommendation_tier
)

def display_model_menu(filter_incompatible=True):
    """Display categorized model menu, optionally filtering by system compatibility"""
    
    # Detect system specs
    specs = get_system_specs()
    max_recommended = get_recommendation_tier(specs)
    
    click.secho("\n" + "="*70, fg="cyan")
    click.secho("iTaK MODEL CATALOG", fg="cyan", bold=True)
    click.secho("="*70, fg="cyan")
    click.secho(f"System: {format_specs_summary(specs)}", fg="white", dim=True)
    click.secho(f"Recommended max size: {max_recommended}B parameters", fg="green")
    click.secho("="*70, fg="cyan")
    
    model_index = 1
    model_map = {}  # Maps index to model name
    hidden_count = 0
    
    for category_name, category_data in OLLAMA_MODEL_CATALOG.items():
        # Collect compatible models for this category
        compatible_models = []
        
        for model_name, model_info in category_data["models"].items():
            compat = get_model_compatibility(model_info, specs)
            if not filter_incompatible or compat != 'incompatible':
                compatible_models.append((model_name, model_info, compat))
            else:
                hidden_count += 1
        
        if not compatible_models:
            continue  # Skip empty categories
        
        # Category header
        click.secho(f"\n{category_name}", fg="yellow", bold=True)
        click.secho(f"   {category_data['description']}", fg="white", dim=True)
        click.secho("-" * 68, fg="white", dim=True)
        
        for model_name, model_info, compat in compatible_models:
            model_map[model_index] = model_name
            
            # Format: [index] model_name (size) - description
            size_str = f"[{model_info['size']}]".ljust(10)
            ctx_str = f"{model_info['ctx']}".ljust(5)
            
            # Check if it's a recommended model
            is_recommended = model_name in RECOMMENDED_MODELS.values()
            
            # Compatibility indicator
            if compat == 'gpu':
                compat_str = "[GPU]"
                compat_color = "green"
            elif compat == 'cpu':
                compat_str = "[CPU]"
                compat_color = "yellow"
            elif compat == 'no_disk':
                compat_str = "[DISK]"
                compat_color = "red"
            else:
                compat_str = "[???]"
                compat_color = "red"
            
            star = "*" if is_recommended else " "
            
            click.secho(f"   {star} ", nl=False)
            click.secho(f"{str(model_index).rjust(2)}. ", fg="green", nl=False)
            click.secho(f"{model_name.ljust(28)}", fg="bright_white", bold=True, nl=False)
            click.secho(f" {size_str}", fg="cyan", nl=False)
            click.secho(f" {compat_str}", fg=compat_color, nl=False)
            click.secho(f" {model_info['desc']}", fg="white", dim=True)
            
            model_index += 1
    
    click.secho("\n" + "="*70, fg="cyan")
    click.secho("* = Recommended | [GPU] = Fast | [CPU] = Slower | [DISK] = Need space", fg="white", dim=True)
    if hidden_count > 0:
        click.secho(f"({hidden_count} models hidden - too large for your system)", fg="white", dim=True)
    click.secho("="*70 + "\n", fg="cyan")
    
    return model_map

def select_models_interactive(filter_incompatible=True):
    """
    Interactive model selection with system-aware filtering.
    Returns list of selected model names.
    """
    model_map = display_model_menu(filter_incompatible)
    total_models = len(model_map)
    
    if total_models == 0:
        click.secho("No compatible models found for your system.", fg="red")
        return []
    
    click.secho("Select models to download:", fg="green", bold=True)
    click.secho("   - Enter numbers separated by commas (e.g., 1,5,12)", fg="white")
    click.secho("   - Enter 'r' for recommended set (system-compatible only)", fg="white")
    click.secho("   - Enter 'a' for all shown models", fg="white")
    click.secho("   - Enter 'q' to skip\n", fg="white")
    
    selection = click.prompt("Your choice", type=str, default="r")
    
    if selection.lower() == 'q':
        return []
    
    if selection.lower() == 'r':
        # Return recommended models that are compatible
        specs = get_system_specs()
        compatible_recommended = []
        for model_name in RECOMMENDED_MODELS.values():
            info = get_model_info(model_name)
            if info:
                compat = get_model_compatibility(info, specs)
                if compat in ('gpu', 'cpu'):
                    compatible_recommended.append(model_name)
        return compatible_recommended
    
    if selection.lower() == 'a':
        if click.confirm(f"Download all {total_models} compatible models?", default=False):
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
                click.secho(f"Invalid number: {idx} (must be 1-{total_models})", fg="yellow")
        return selected
    except ValueError:
        click.secho("Invalid input. Please enter numbers separated by commas.", fg="red")
        return []

def download_models(model_names, show_progress=True):
    """
    Download multiple models from Ollama.
    Returns dict of {model_name: success_bool}
    """
    results = {}
    total = len(model_names)
    
    if total == 0:
        click.secho("No models selected.", fg="yellow")
        return results
    
    click.secho(f"\nDownloading {total} model(s)...\n", fg="cyan", bold=True)
    
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
                click.secho(f"   [OK] {model_name} downloaded!", fg="green")
                results[model_name] = True
            else:
                click.secho(f"   [FAIL] Failed to download {model_name}", fg="red")
                results[model_name] = False
        except Exception as e:
            click.secho(f"   [ERROR] {e}", fg="red")
            results[model_name] = False
    
    # Summary
    success_count = sum(1 for v in results.values() if v)
    click.secho(f"\n{'='*70}", fg="cyan")
    click.secho(f"Download Summary: {success_count}/{total} successful", 
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
        
        click.secho(f"Model '{model_name}' not found locally.", fg="yellow")
        click.secho(f"   Downloading {model_name} ({size_str})...", fg="yellow")
        click.secho("   (This may take a few minutes on first run)", fg="white", dim=True)
        
        result = subprocess.run(["ollama", "pull", model_name], capture_output=False)
        
        if result.returncode == 0:
            click.secho(f"[OK] Model '{model_name}' downloaded!", fg="green")
            return True
        else:
            click.secho(f"[FAIL] Failed to download '{model_name}'", fg="red")
            return False
            
    except Exception as e:
        click.secho(f"Could not check models: {e}", fg="yellow")
        return False

def get_quick_model_selection():
    """Quick model selection based on system capabilities"""
    specs = get_system_specs()
    max_tier = get_recommendation_tier(specs)
    
    click.secho("\nQuick Model Selection:", fg="cyan", bold=True)
    click.secho(f"System: {format_specs_summary(specs)}", fg="white", dim=True)
    click.secho("="*50, fg="cyan")
    
    # Build options based on what the system can run
    all_options = [
        (14, "1", "qwen2.5-coder:14b", "[CODING] Advanced coding (9GB)"),
        (7, "2", "qwen2.5-coder:7b", "[CODING] Strong coding (4.7GB)"),
        (3, "3", "qwen2.5-coder:3b", "[CODING] Efficient coding (1.9GB)"),
        (8, "4", "deepseek-r1:8b", "[REASONING] Deep reasoning (5.2GB)"),
        (8, "5", "qwen3:8b", "[GENERAL] General purpose (5.2GB)"),
        (4, "6", "qwen3:4b", "[GENERAL] Efficient general (2.5GB)"),
        (8, "7", "qwen3-vl:8b", "[VISION] Vision analysis (6.1GB)"),
        (1.7, "8", "smollm2:1.7b", "[LIGHT] Lightweight (1.8GB)"),
    ]
    
    # Filter to models that can run on this system
    available_options = []
    for size_b, opt, model, desc in all_options:
        if size_b <= max_tier:
            available_options.append((opt, model, desc))
    
    if not available_options:
        # Fallback to smallest
        available_options = [("1", "smollm2:135m", "[LIGHT] Tiny (271MB)")]
    
    # Add catalog option
    available_options.append(("c", None, "[CATALOG] Show full catalog"))
    
    for opt, model, desc in available_options:
        click.secho(f"  {opt}. ", fg="green", nl=False)
        click.secho(desc, fg="white")
    
    choice = click.prompt("\nSelect", type=str, default="2" if len(available_options) > 2 else "1")
    
    if choice == 'c':
        selected = select_models_interactive()
        return selected[0] if selected else available_options[0][1]
    
    for opt, model, _ in available_options:
        if choice == opt and model:
            return model
    
    # Return best available
    return available_options[0][1] if available_options[0][1] else "smollm2:1.7b"
