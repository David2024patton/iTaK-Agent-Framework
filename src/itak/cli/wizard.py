"""
iTaK Project Creation Wizard

Interactive CLI wizard for creating new projects.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click


class BackToMenu(Exception):
    """Raised when user wants to go back to main menu."""
    pass


def is_back_command(text: str) -> bool:
    """Check if input is a back/exit command."""
    if text is None:
        return False
    cmd = text.strip().lower()
    cmd = text.strip().lower()
    return cmd in ['back', '/back', '0', 'exit', '/exit', '/quit']  # Include exit commands


def wizard_prompt(label: str, default: str = "") -> str:
    """Prompt that checks for back/exit commands."""
    click.echo(f"  {click.style('(type 0 or back to cancel)', fg='bright_black')}")
    result = click.prompt(click.style(f"  {label}", fg="cyan"), type=str, default=default)
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
        default_desc = "A new iTaK project"
        
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
            description = wizard_prompt("  What should it do", default_desc)
        
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
            # If we detected a type and have initial_prompt, use it automatically
            if detected_type_idx and initial_prompt:
                project_type = PROJECT_TYPES[detected_type_idx - 1]
                click.secho(f"  🎯 Detected type: {project_type[0]}", fg="green")
            else:
                # Ask user to select
                click.secho("  🎯 Select project type:", fg="white", bold=True)
                click.echo()
                for i, (name, _, desc) in enumerate(PROJECT_TYPES, 1):
                    click.secho(f"      [{i}] ", fg="cyan", nl=False)
                    click.secho(name, fg="white", bold=True, nl=False)
                    click.secho(f"  {desc}", fg="bright_black")
                click.echo()
                
                # Show detected suggestion if any
                if detected_type_idx:
                    click.secho(f"  💡 Suggested: [{detected_type_idx}] based on description", fg="yellow")
                
                while True:
                    type_input = click.prompt(
                        click.style("  Choice", fg="cyan"),
                        type=str,
                        default=str(detected_type_idx) if detected_type_idx else "1"
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
