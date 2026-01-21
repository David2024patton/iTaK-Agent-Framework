# iTaK First-Run Auto-Setup
# Automatically installs all dependencies and default model on first run

import subprocess
import sys
import os
import json
from pathlib import Path

import click

# Configuration
SETUP_MARKER = Path.home() / ".itak" / ".setup_complete"
CONFIG_FILE = Path.home() / ".itak" / "config.json"
DEFAULT_MODEL = "ollama/qwen3-vl:2b"
DEFAULT_MODEL_SIZE = "3.3GB"


def is_first_run():
    """Check if this is the first time running iTaK"""
    return not SETUP_MARKER.exists()


def mark_setup_complete():
    """Mark that setup has been completed"""
    SETUP_MARKER.parent.mkdir(parents=True, exist_ok=True)
    SETUP_MARKER.write_text("1")


def get_config() -> dict:
    """Load config from file."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except:
            return {}
    return {}


def save_config(config: dict):
    """Save config to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def check_and_install_package(package_name, import_name=None, quiet=False):
    """Check if a package is installed, install if missing"""
    import_name = import_name or package_name
    try:
        __import__(import_name)
        return True
    except ImportError:
        if not quiet:
            print(f"  Installing {package_name}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", package_name],
                stdout=subprocess.DEVNULL if quiet else None,
                stderr=subprocess.DEVNULL if quiet else None
            )
            return True
        except:
            return False


def check_ollama_installed() -> bool:
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False


def check_model_installed(model: str) -> bool:
    """Check if a specific model is already installed."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return model.split(":")[0] in result.stdout
    except:
        return False


def install_default_model(model: str = DEFAULT_MODEL) -> bool:
    """Pull the default model via Ollama."""
    click.echo()
    click.secho(f"  📦 Installing default model: {model} ({DEFAULT_MODEL_SIZE})...", fg="cyan")
    click.echo()
    
    try:
        result = subprocess.run(
            ["ollama", "pull", model],
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            click.secho("  ✅ Model installed successfully!", fg="green")
            return True
        else:
            click.secho("  ❌ Failed to install model", fg="red")
            return False
    except subprocess.TimeoutExpired:
        click.secho("  ⏱️ Model download timed out", fg="yellow")
        return False
    except Exception as e:
        click.secho(f"  ❌ Error: {e}", fg="red")
        return False


def show_welcome_screen():
    """Display the welcome screen with ASCII art."""
    click.clear()
    
    # Header
    click.secho("╔" + "═" * 62 + "╗", fg="cyan", bold=True)
    click.secho("║" + " " * 62 + "║", fg="cyan")
    click.secho("║   🚀 ", fg="cyan", nl=False)
    click.secho("Welcome to iTaK Agent Framework", fg="white", bold=True, nl=False)
    click.secho(" " * 18 + "║", fg="cyan")
    click.secho("║   " + "─" * 56 + "   ║", fg="cyan")
    click.secho("║   ", fg="cyan", nl=False)
    click.secho("Intelligent Task Automation Kernel", fg="yellow", nl=False)
    click.secho(" " * 20 + "║", fg="cyan")
    click.secho("║" + " " * 62 + "║", fg="cyan")
    click.secho("╚" + "═" * 62 + "╝", fg="cyan", bold=True)
    click.echo()


def show_menu() -> int:
    """Display the interactive menu and get user choice."""
    click.secho("╔" + "═" * 62 + "╗", fg="blue")
    click.secho("║  ", fg="blue", nl=False)
    click.secho("How would you like to continue?", fg="white", bold=True, nl=False)
    click.secho(" " * 26 + "║", fg="blue")
    click.secho("║" + " " * 62 + "║", fg="blue")
    
    click.secho("║  ", fg="blue", nl=False)
    click.secho("[1]", fg="green", bold=True, nl=False)
    click.secho(" 🌐 Open Studio (Web UI)", fg="white", nl=False)
    click.secho(" " * 30 + "║", fg="blue")
    
    click.secho("║      ", fg="blue", nl=False)
    click.secho("→ Launch browser-based interface", fg="bright_black", nl=False)
    click.secho(" " * 23 + "║", fg="blue")
    click.secho("║" + " " * 62 + "║", fg="blue")
    
    click.secho("║  ", fg="blue", nl=False)
    click.secho("[2]", fg="green", bold=True, nl=False)
    click.secho(" 💻 Continue in CLI", fg="white", nl=False)
    click.secho(" " * 35 + "║", fg="blue")
    
    click.secho("║      ", fg="blue", nl=False)
    click.secho("→ Create your first project", fg="bright_black", nl=False)
    click.secho(" " * 28 + "║", fg="blue")
    click.secho("║" + " " * 62 + "║", fg="blue")
    
    click.secho("║  ", fg="blue", nl=False)
    click.secho("[3]", fg="green", bold=True, nl=False)
    click.secho(" 📚 View Model Catalog", fg="white", nl=False)
    click.secho(" " * 32 + "║", fg="blue")
    
    click.secho("║      ", fg="blue", nl=False)
    click.secho("→ Browse 100+ models across 20 domains", fg="bright_black", nl=False)
    click.secho(" " * 16 + "║", fg="blue")
    click.secho("║" + " " * 62 + "║", fg="blue")
    
    click.secho("║  ", fg="blue", nl=False)
    click.secho("[4]", fg="green", bold=True, nl=False)
    click.secho(" ❓ Help / Documentation", fg="white", nl=False)
    click.secho(" " * 30 + "║", fg="blue")
    click.secho("║" + " " * 62 + "║", fg="blue")
    
    click.secho("╚" + "═" * 62 + "╝", fg="blue")
    click.echo()
    
    while True:
        choice = click.prompt(
            click.style("  Enter choice", fg="cyan"),
            type=int,
            default=2
        )
        if 1 <= choice <= 4:
            return choice
        click.secho("  Please enter 1, 2, 3, or 4", fg="yellow")


def show_help():
    """Display help information."""
    click.echo()
    click.secho("  📖 iTaK Quick Reference", fg="cyan", bold=True)
    click.echo()
    click.secho("  Commands:", fg="white", bold=True)
    click.echo("    itak auto \"prompt\"     - Build something with AI")
    click.echo("    itak models --list     - Show all available models")
    click.echo("    itak models --select   - Interactive model selection")
    click.echo("    itak create            - Create a new project")
    click.echo()
    click.secho("  Examples:", fg="white", bold=True)
    click.echo('    itak auto "Build a todo list web app"')
    click.echo('    itak auto "Create a Python web scraper for news sites"')
    click.echo('    itak auto "Analyze this screenshot" --image ./screen.png')
    click.echo()
    click.secho("  Documentation:", fg="white", bold=True)
    click.echo("    https://github.com/David2024patton/iTaK-Agent-Framework")
    click.echo()


def handle_menu_choice(choice: int):
    """Handle the user's menu selection."""
    if choice == 1:
        # Open Studio
        click.echo()
        click.secho("  🌐 Opening Studio...", fg="cyan")
        try:
            from itak.cli.studio_launcher import launch_studio
            launch_studio()
        except ImportError:
            click.secho("  Note: Studio is coming soon!", fg="yellow")
            click.secho("  For now, use the CLI with: itak auto \"your prompt\"", fg="white")
        
    elif choice == 2:
        # Continue to project wizard
        try:
            from itak.cli.wizard import run_project_wizard
            run_project_wizard()
        except ImportError:
            click.echo()
            click.secho("  💻 Ready to build!", fg="green")
            click.echo()
            click.echo("  Run: itak auto \"describe what you want to build\"")
            click.echo()
        
    elif choice == 3:
        # Show model catalog
        try:
            from itak.cli.model_selector import display_model_menu
            click.echo()
            display_model_menu()
        except ImportError:
            click.secho("  Model catalog not available", fg="yellow")
        
    elif choice == 4:
        # Show help
        show_help()


def auto_setup(force=False):
    """
    Auto-install all iTaK dependencies on first run.
    Called automatically when any itak command is run.
    """
    if not force and not is_first_run():
        return True
    
    # Show fancy welcome screen
    show_welcome_screen()
    
    click.secho("  🔧 First-time setup...", fg="cyan", bold=True)
    click.echo()
    
    # Check Ollama
    if not check_ollama_installed():
        click.secho("  ⚠️  Ollama not detected!", fg="yellow", bold=True)
        click.echo()
        click.echo("  Please install Ollama first:")
        click.secho("  → https://ollama.com/download", fg="cyan")
        click.echo()
        click.echo("  Then run 'itak' again.")
        click.echo()
        mark_setup_complete()  # Still mark complete to not block
        return True
    
    click.secho("  ✅ Ollama detected", fg="green")
    
    # Install dependencies silently
    success = True
    core_packages = [
        ("click", "click"),
        ("rich", "rich"),
        ("pyyaml", "yaml"),
        ("requests", "requests"),
        ("httpx", "httpx"),
    ]
    
    for package, import_name in core_packages:
        try:
            __import__(import_name)
        except ImportError:
            if not check_and_install_package(package, import_name, quiet=True):
                success = False
    
    # Check/install default model
    if not check_model_installed(DEFAULT_MODEL):
        install_default_model()
    else:
        click.secho(f"  ✅ Default model ({DEFAULT_MODEL}) ready", fg="green")
    
    click.echo()
    
    # Save config
    config = get_config()
    config["first_run_complete"] = True
    config["default_model"] = DEFAULT_MODEL
    save_config(config)
    
    # Mark setup complete
    mark_setup_complete()
    
    return success


def reset_setup():
    """Reset the setup marker to force re-run on next command"""
    if SETUP_MARKER.exists():
        SETUP_MARKER.unlink()
        return True
    return False
