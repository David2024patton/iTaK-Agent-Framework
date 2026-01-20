"""
iTaK Project Creation Wizard

Interactive CLI wizard for creating new projects.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

import click


PROJECT_TYPES = [
    ("🌐 Web App", "web", "HTML/CSS/JavaScript web application"),
    ("🐍 Python Script", "python", "Python script or automation"),
    ("⚡ API/Backend", "api", "REST API or backend service"),
    ("🤖 AI Agent", "agent", "AI agent or automation workflow"),
    ("📝 Custom", "custom", "Describe your project freely"),
]


def run_project_wizard(initial_prompt: str = None, project_type_idx: int = None):
    """Run the interactive project creation wizard."""
    # Box: "📁 Create New Project" = ~22 chars visible + padding
    title = "📁 Create New Project"
    box_width = 28
    
    click.echo()
    click.secho("  ╔" + "═" * box_width + "╗", fg="magenta")
    click.secho("  ║ ", fg="magenta", nl=False)
    click.secho(title, fg="white", bold=True, nl=False)
    click.secho(" " * (box_width - len(title) - 1) + "║", fg="magenta")
    click.secho("  ╚" + "═" * box_width + "╝", fg="magenta")
    click.echo()
    
    # Infer defaults from initial prompt
    default_name = "my-project"
    default_desc = "A new iTaK project"
    
    if initial_prompt:
        # Simple heuristic to extract potential name
        # e.g. "Build a finance dashboard" -> "finance-dashboard"
        words = initial_prompt.lower().split()
        ignored = {'build', 'create', 'make', 'a', 'an', 'new', 'with', 'using', 'for'}
        meaningful = [w for w in words if w not in ignored]
        if meaningful:
            default_name = "-".join(meaningful[:3])
            
        default_desc = initial_prompt
    
    # Project name
    project_name = click.prompt(
        click.style("  Project name", fg="cyan"),
        type=str,
        default=default_name
    )
    
    # Description (Skip if we already have it from initial_prompt)
    if initial_prompt:
        description = initial_prompt
    else:
        description = click.prompt(
            click.style("  Description", fg="cyan"),
            type=str,
            default=default_desc
        )
    
    click.echo()
    
    # Project type
    if project_type_idx is None:
        click.secho("  What type of project?", fg="white", bold=True)
        click.echo()
        for i, (name, _, desc) in enumerate(PROJECT_TYPES, 1):
            click.secho(f"    [{i}] ", fg="green", nl=False)
            click.secho(name, fg="white", nl=False)
            click.secho(f" - {desc}", fg="bright_black")
        click.echo()
        
        while True:
            type_choice = click.prompt(
                click.style("  Choice", fg="cyan"),
                type=int,
                default=1
            )
            if 1 <= type_choice <= len(PROJECT_TYPES):
                break
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
            custom_prompt = click.prompt(
                click.style("  Describe what you want to build", fg="cyan"),
                type=str
            )
    
    click.echo()
    
    # Output directory
    default_dir = f"./{project_name}"
    output_dir = click.prompt(
        click.style("  Output directory", fg="cyan"),
        type=str,
        default=default_dir
    )
    
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


def start_build(prompt: str, output_dir: str):
    """Start the build process with iTaK auto."""
    click.secho("  🚀 Starting build...", fg="cyan", bold=True)
    click.echo()
    click.secho(f"  Prompt: ", fg="white", nl=False)
    click.secho(prompt[:80] + "..." if len(prompt) > 80 else prompt, fg="bright_black")
    click.echo()
    
    # Create output directory
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        click.secho(f"  ⚠️ Could not create directory: {e}", fg="yellow")
        output_dir = "."
    
    # Run itak auto command via subprocess
    click.secho("  Running: ", fg="white", nl=False)
    click.secho(f'itak auto "..."', fg="cyan")
    click.echo()
    
    try:
        import subprocess
        import sys
        
        # Run itak auto as subprocess
        result = subprocess.run(
            [sys.executable, "-m", "itak.cli.cli", "auto", prompt],
            cwd=output_dir,
            shell=False
        )
        
        if result.returncode == 0:
            click.secho("  ✅ Build complete!", fg="green")
        else:
            click.secho(f"  ⚠️ Build finished with code {result.returncode}", fg="yellow")
            
    except Exception as e:
        click.secho(f"  ❌ Error: {e}", fg="red")
        click.echo()
        click.echo("  To run manually:")
        click.secho(f'  cd {output_dir}', fg="cyan")
        click.secho(f'  itak auto "{prompt}"', fg="cyan")


if __name__ == "__main__":
    run_project_wizard()
