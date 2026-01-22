"""
iTaK Project Creation Wizard

Interactive CLI wizard for creating new projects.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Optional
from .guild_auto import get_or_create_guild_for_project, run_guild_build
from .agent_manager import initialize_default_wizards

import click


class BackToMenu(Exception):
    """Raised when user wants to go back to main menu."""
    pass


class ExitCLI(Exception):
    """Raised when user wants to exit the CLI completely."""
    pass


def is_back_command(text: str) -> bool:
    """Check if input is a back command (returns to menu)."""
    if text is None:
        return False
    cmd = text.strip().lower()
    return cmd in ['back', '/back', '0']


def is_exit_command(text: str) -> bool:
    """Check if input is an exit command (exits CLI completely)."""
    if text is None:
        return False
    cmd = text.strip().lower()
    return cmd in ['exit', '/exit', '/quit', 'quit']


def wizard_prompt(label: str, default: str = "") -> str:
    """Prompt that checks for back/exit commands."""
    click.echo(f"  {click.style('(type 0 or back to cancel, /exit to quit)', fg='bright_black')}")
    result = click.prompt(click.style(f"  {label}", fg="cyan"), type=str, default=default)
    if is_exit_command(result):
        raise ExitCLI()
    if is_back_command(result):
        raise BackToMenu()
    return result


PROJECT_TYPES = [
    ("🌐 Web App", "web", "HTML/CSS/JavaScript web application"),
    ("🐍 Python Script", "python", "Python script or automation"),
    ("⚡ API/Backend", "api", "REST API or backend service"),
    ("🤖 AI Agent", "agent", "AI agent or automation workflow"),
    ("📝 Custom", "custom", "Describe your project freely"),
]


def run_project_wizard(initial_prompt: str = None, project_type_idx: int = None):
    """Run the interactive project creation wizard."""
    click.echo()
    
    # Header
    click.secho("  ╔══════════════════════════════════════════════════════════════╗", fg="magenta")
    click.secho("  ║", fg="magenta", nl=False)
    click.secho("  🧙 Wizard Code", fg="yellow", bold=True, nl=False)
    click.secho(" - Not Vibe Code... Wizard Code", fg="white", nl=False)
    click.secho("               ║", fg="magenta")
    click.secho("  ╚══════════════════════════════════════════════════════════════╝", fg="magenta")
    click.echo()
    
    # Show project type examples
    click.secho("  ┌───────────────────────────────────────────────────────────────┐", fg="bright_black")
    click.secho("  │  💡 What can you build?                                       │", fg="bright_black")
    click.secho("  │                                                               │", fg="bright_black")
    click.secho("  │    🌐 Web Apps    → React dashboards, landing pages           │", fg="bright_black")
    click.secho("  │    🐍 Python      → Data scripts, web scrapers, automation    │", fg="bright_black")
    click.secho("  │    ⚡ APIs        → FastAPI backends, REST services           │", fg="bright_black")
    click.secho("  │    🤖 AI Agents   → CrewAI workflows, chatbots                │", fg="bright_black")
    click.secho("  │    📝 Custom      → Describe anything, AI figures it out      │", fg="bright_black")
    click.secho("  │                                                               │", fg="bright_black")
    click.secho("  └───────────────────────────────────────────────────────────────┘", fg="bright_black")
    click.echo()
    
    click.secho("  (type 0 or back to cancel)", fg="bright_black")
    click.echo()
    
    try:
        # Infer defaults from initial prompt
        default_name = "my-project"
        default_desc = ""  # No default - user must describe project
        
        if initial_prompt:
            # Simple heuristic to extract potential name
            # e.g. "Build a finance dashboard" -> "finance-dashboard"
            words = initial_prompt.lower().split()
            ignored = {'build', 'create', 'make', 'a', 'an', 'new', 'with', 'using', 'for', 'project'}
            meaningful = [w for w in words if w not in ignored]
            
            # Only auto-fill name if it looks like a short intent (<= 5 words total)
            # If it's a long description, just default to general name
            if meaningful and len(words) < 10:
                default_name = "-".join(meaningful[:3])
            
            default_desc = initial_prompt
        
        # Project name
        # If default name comes from a long prompt, reset it to safe default
        if len(default_name) > 30: 
            default_name = "my-project"
            
        click.secho("  📁 Project Setup", fg="white", bold=True)
        click.echo()
        click.secho("  💡 Tip: Type as much as you want, it will wrap nicely", fg="bright_black")
        click.echo()
        project_name = wizard_prompt("  Project name", default_name)
    
        # Description (Skip if we already have it from initial_prompt)
        if initial_prompt:
            description = initial_prompt
        else:

            # Force user to enter a description (required for auto-detection)

            while True:

                description = wizard_prompt("  What should it do", default_desc)

                if description.strip():  # Non-empty after stripping whitespace
                    # Show wrapped version for better readability
                    if len(description) > 70:
                        click.echo()
                        click.secho("  📝 Description:", fg="bright_black")
                        wrapped = textwrap.fill(description, width=70, initial_indent="  ", subsequent_indent="  ")
                        click.secho(wrapped, fg="white")
                    break

                click.secho("  ⚠️  Please describe what your project should do", fg="yellow")

                click.echo()

        
        click.echo()
        
        # Smart project type detection from description
        detected_type_idx = None
        if description:
            desc_lower = description.lower()
            
            # Keyword matching for project types
            if any(word in desc_lower for word in ['website', 'web app', 'landing page', 'dashboard', 'frontend', 'react', 'html', 'css']):
                detected_type_idx = 1  # Web App
            elif any(word in desc_lower for word in ['api', 'backend', 'rest', 'fastapi', 'flask', 'server', 'endpoint']):
                detected_type_idx = 3  # API/Backend
            elif any(word in desc_lower for word in ['agent', 'bot', 'automation', 'workflow', 'ai agent', 'crew']):
                detected_type_idx = 4  # AI Agent  
            elif any(word in desc_lower for word in ['script', 'python', 'automation', 'scraper', 'tool']):
                detected_type_idx = 2  # Python Script
        
        # Project type
        if project_type_idx is None:
            # If we detected a type, use it automatically (skip selection)
            if detected_type_idx:
                project_type = PROJECT_TYPES[detected_type_idx - 1]
                click.secho(f"  🎯 Detected type: {project_type[0]}", fg="green")
                click.echo()
            else:
                # Ask user to select
                click.secho("  🎯 Select project type:", fg="white", bold=True)
                click.echo()
                for i, (name, _, desc) in enumerate(PROJECT_TYPES, 1):
                    click.secho(f"      [{i}] ", fg="cyan", nl=False)
                    click.secho(name, fg="white", bold=True, nl=False)
                    click.secho(f"  {desc}", fg="bright_black")
                click.echo()
                
                while True:
                    type_input = click.prompt(
                        click.style("  Choice", fg="cyan"),
                        type=str,
                        default="1"
                    )
                    if is_back_command(type_input):
                        raise BackToMenu()
                    try:
                        type_choice = int(type_input)
                        if 1 <= type_choice <= len(PROJECT_TYPES):
                            break
                    except ValueError:
                        pass
                    click.secho("  Please enter a valid number", fg="yellow")
                
                project_type = PROJECT_TYPES[type_choice - 1]
        else:
            # Use pre-selected type (adjusted for 0-index if passing from menu that might use 1-index)
            # But wait, let's assume valid PROJECT_TYPES index + 1 is passed or just index
            project_type = PROJECT_TYPES[project_type_idx - 1]
            click.secho(f"  Selected: {project_type[0]}", fg="green")
        
        # Custom description if needed
        custom_prompt = None
        if project_type[1] == "custom":
            if initial_prompt:
                custom_prompt = initial_prompt
            else:
                custom_prompt = wizard_prompt("Describe what you want to build", "")
        
        click.echo()
        
        # Output directory
        default_dir = f"./{project_name}"
        output_dir = wizard_prompt("Output directory", default_dir)
        
        # Confirm
        click.echo()
        click.secho("  ─" * 30, fg="bright_black")
        click.echo()
        click.secho("  📋 Project Summary:", fg="white", bold=True)
        click.echo(f"      Name: {project_name}")
        click.echo(f"      Type: {project_type[0]}")
        click.echo(f"      Description: {description}")
        click.echo(f"      Output: {output_dir}")
        click.echo()
        
        if not click.confirm(click.style("  Start building?", fg="cyan"), default=True):
            click.secho("  Cancelled.", fg="yellow")
            return
        
        click.echo()
        
        # Build the prompt
        if custom_prompt:
            full_prompt = custom_prompt
        else:
            full_prompt = build_prompt(project_name, description, project_type)
        
        # Run iTaK auto
        start_build(full_prompt, output_dir)
    
    except BackToMenu:
        click.secho("\n  Cancelled. Returning to menu...\n", fg="yellow")
        return


def build_prompt(name: str, description: str, project_type: tuple) -> str:
    """Build the prompt for the AI based on project type."""
    type_name, type_key, _ = project_type
    
    prompts = {
        "web": f"Build a {description}. Create a complete web application with HTML, CSS, and JavaScript. Include a modern, attractive design with responsive layout. Name: {name}",
        
        "python": f"Create a Python script for: {description}. Include proper error handling, docstrings, and a main function. Make it production-ready. Name: {name}",
        
        "api": f"Build a REST API for: {description}. Use FastAPI or Flask. Include proper endpoints, error handling, and basic documentation. Name: {name}",
        
        "agent": f"Create an AI agent workflow for: {description}. Use iTaK's multi-agent architecture with appropriate agents for the task. Name: {name}",
    }
    
    return prompts.get(type_key, description)


def start_build(prompt: str, output_dir: str, project_type: str = 'custom'):
    """Start the build process using guild system."""
    import click
    
    # Initialize default wizards if they don't exist
    click.secho("  🔮 Initializing wizards...", fg="magenta")
    initialize_default_wizards()
    
    click.secho("  🚀 Starting guild build...",  fg="cyan", bold=True)
    click.echo()
    click.secho(f"  Project: ", fg="white", nl=False)
    click.secho(prompt[:70] + "..." if len(prompt) > 70 else prompt, fg="bright_black")
    click.echo()
    
    # Create output directory
    try:
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        click.secho(f"  ⚠️  Could not create directory: {e}", fg="yellow")
        output_dir = "."
    
    # Get or create appropriate guild
    guild_name = get_or_create_guild_for_project(project_type, prompt)
    
    # Run guild build
    run_guild_build(guild_name, prompt, output_dir)


if __name__ == "__main__":
    run_project_wizard()

