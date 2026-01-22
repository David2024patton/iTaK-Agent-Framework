"""
Auto-Guild System for iTaK Wizard Code

Automatically creates and runs guilds (teams of wizards) based on project type.
Uses sequential LiteAgent execution for multi-agent collaboration.
"""

import os
import yaml
from pathlib import Path
from typing import Optional, List
import click

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
    Run a guild to build a project using sequential LiteAgent execution.
    
    Args:
        guild_name: Name of the guild (without .yaml)
        project_description: What to build
        output_dir: Where to create files
    """
    from itak.lite_agent import LiteAgent
    from itak.tools.agent_tools.file_tools import (
        FileReadTool,
        FileWriteTool,
    )
    from itak.tools.agent_tools.code_search import RipGrepTool
    from itak.tools.agent_tools.code_editor import SmartEditTool
    
    # Load guild configuration
    guild_file = CREWS_DIR / f"{guild_name}.yaml"
    
    if not guild_file.exists():
        click.secho(f"\n  ❌ Guild not found: {guild_name}", fg="red")
        return
    
    with open(guild_file) as f:
        guild = yaml.safe_load(f)
    
    # Load wizard configurations
    wizard_configs = []
    click.secho(f"\n  🏰 Assembling {guild['name']}...", fg="magenta")
    
    for wizard_id in guild.get('agents', []):
        wizard_file = AGENTS_DIR / f"{wizard_id}.yaml"
        
        if not wizard_file.exists():
            click.secho(f"  ⚠️  Wizard not found: {wizard_id}", fg="yellow")
            continue
        
        with open(wizard_file) as f:
            wizard = yaml.safe_load(f)
        
        click.secho(f"  ✓ {wizard.get('name', wizard_id)} ready", fg="green")
        wizard_configs.append(wizard)
    
    if not wizard_configs:
        click.secho("\n  ❌ No wizards available. Run 'itak' → [3] Wizards to create some first.", fg="red")
        return
    
    click.secho(f"\n  🚀 Starting {len(wizard_configs)}-wizard collaboration...", fg="cyan")
    click.secho(f"  📋 Project: {project_description}", fg="white")
    click.secho(f"  📁 Output: {output_dir}\n", fg="white")
    
    # Initialize tool registry
    all_tools = {
        'file_read': FileReadTool(),
        'file_write': FileWriteTool(),
        'code_search': RipGrepTool(),
        'smart_edit': SmartEditTool(),
    }
    
    # Run wizards sequentially, passing context between them
    previous_output = ""
    
    for i, wizard_config in enumerate(wizard_configs, 1):
        wizard_name = wizard_config.get('name', 'Unknown')
        wizard_role = wizard_config.get('role', 'Developer')
        wizard_goal = wizard_config.get('goal', 'Complete the task')
        backstory = wizard_config.get('backstory', 'An expert in their field')
        tool_names = wizard_config.get('tools', [])
        llm = wizard_config.get('llm', 'ollama/qwen3-vl:2b')
        
        click.secho(f"\n  🔮 [{i}/{len(wizard_configs)}] {wizard_name} working...", fg="magenta")
        
        # Map tool names to actual tool instances
        wizard_tools = [all_tools[name] for name in tool_names if name in all_tools]
        
        # Create task based on wizard role and previous output
        if i == 1:
            # First wizard: Plan the project
            task = f"{project_description}. Working directory: {output_dir}. Create a plan and start building."
        else:
            # Subsequent wizards: Build on previous work
            task = f"Continue working on: {project_description}. Working directory: {output_dir}.\n\nPrevious work:\n{previous_output}"
        
        # Create and run the wizard
        try:
            wizard_agent = LiteAgent(
                role=wizard_role,
                goal=wizard_goal,
                backstory=backstory,
                tools=wizard_tools,
                llm=llm,
                verbose=False,
                max_iterations=10,
            )
            
            result = wizard_agent.kickoff(task)
            previous_output = result.raw
            
            click.secho(f"  ✓ {wizard_name} complete", fg="green")
            
        except Exception as e:
            click.secho(f"  ❌ {wizard_name} failed: {e}", fg="red")
            continue
    
    click.secho(f"\n  ✅ Guild collaboration complete!", fg="green", bold=True)
    click.secho(f"  📁 Check {output_dir} for generated files\n", fg="cyan")
