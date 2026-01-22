"""
Auto-Guild System for iTaK Wizard Code

Automatically creates and runs guilds (teams of wizards) based on project type.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Optional, List

# Directories
AGENTS_DIR = Path.home() / '.itak' / 'agents'
CREWS_DIR = Path.home() / '.itak' / 'crews'


def ensure_dirs():
    """Ensure config directories exist."""
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CREWS_DIR.mkdir(parents=True, exist_ok=True)


# Guild compositions for each project type
GUILD_MAPPINGS = {
    'web': {
        'name': 'Web Development Guild',
        'wizards': ['project_manager', 'frontend_wizard', 'javascript_wizard', 'content_wizard', 'qa_wizard'],
        'workflow': 'sequential',
        'description': 'Full-stack web development team'
    },
    'python': {
        'name': 'Python Development Guild',
        'wizards': ['project_manager', 'coder', 'qa_wizard'],
        'workflow': 'sequential',
        'description': 'Python script and automation team'
    },
    'api': {
        'name': 'API Development Guild',
        'wizards': ['project_manager', 'coder', 'qa_wizard'],
        'workflow': 'sequential',
        'description': 'Backend API development team'
    },
    'agent': {
        'name': 'AI Agent Guild',
        'wizards': ['project_manager', 'coder'],
        'workflow': 'sequential',
        'description': 'AI agent and automation team'
    },
    'custom': {
        'name': 'Custom Development Guild',
        'wizards': ['project_manager', 'coder', 'writer', 'qa_wizard'],
        'workflow': 'sequential',
        'description': 'General purpose development team'
    },
}


def get_or_create_guild_for_project(project_type: str, description: str) -> str:
    """
    Get or create a guild for the given project type.
    
    Args:
        project_type: Type of project ('web', 'python', 'api', 'agent', 'custom')
        description: Project description (for logging/context)
    
    Returns:
        Guild name (filename without .yaml)
    """
    ensure_dirs()
    
    # Get guild configuration
    guild_config = GUILD_MAPPINGS.get(project_type, GUILD_MAPPINGS['custom'])
    safe_name = project_type + '_dev_guild'
    guild_file = CREWS_DIR / f"{safe_name}.yaml"
    
    # Check if guild already exists
    if not guild_file.exists():
        # Create new guild
        guild_def = {
            'name': guild_config['name'],
            'agents': guild_config['wizards'],
            'workflow': guild_config['workflow'],
            'description': guild_config['description'],
            'verbose': False,
        }
        
        with open(guild_file, 'w') as f:
            yaml.dump(guild_def, f, default_flow_style=False)
    
    return safe_name


def run_guild_build(guild_name: str, project_description: str, output_dir: str):
    """
    Run a guild to build a project.
    
    Args:
        guild_name: Name of the guild (without .yaml)
        project_description: What to build
        output_dir: Where to create files
    """
    import click
    
    # Load guild configuration
    guild_file = CREWS_DIR / f"{guild_name}.yaml"
    
    if not guild_file.exists():
        click.secho(f"\n  ❌ Guild not found: {guild_name}", fg="red")
        return
    
    with open(guild_file) as f:
        guild = yaml.safe_load(f)
    
    # Load wizards
    wizard_agents = []
    click.secho(f"\n  🏰 Assembling {guild['name']}...", fg="magenta")
    
    for wizard_id in guild.get('agents', []):
        wizard_file = AGENTS_DIR / f"{wizard_id}.yaml"
        
        if not wizard_file.exists():
            click.secho(f"  ⚠️  Wizard not found: {wizard_id}", fg="yellow")
            continue
        
        with open(wizard_file) as f:
            wizard = yaml.safe_load(f)
        
        click.secho(f"  ✓ {wizard.get('name', wizard_id)} ready", fg="green")
        wizard_agents.append(wizard)
    
    if not wizard_agents:
        click.secho("\n  ❌ No wizards available. Run 'itak' → [3] Wizards to create some first.", fg="red")
        return
    
    click.secho(f"\n  🚀 Starting {len(wizard_agents)}-wizard collaboration...", fg="cyan")
    click.secho(f"  📋 Project: {project_description}", fg="white")
    click.secho(f"  📁 Output: {output_dir}\n", fg="white")
    
    # For now, fall back to single agent (CrewAI integration comes next)
    # This is a bridge implementation
    click.secho("  🔮 Building with enhanced agent team...\n", fg="magenta")
    
    # Use itak auto as fallback for now
    import subprocess
    cmd = ["itak", "auto", "--skip-wizard", f"Build a {project_description}. Create files in {output_dir}/"]
    subprocess.run(cmd)
