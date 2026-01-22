"""
Auto-Guild System for iTaK Wizard Code

Automatically creates and runs guilds (teams of wizards) based on project type.
Uses sequential LiteAgent execution for multi-agent collaboration.
"""

import yaml
from pathlib import Path
import click
import os

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
    """Get or create a guild for the given project type."""
    ensure_dirs()
    guild_config = GUILD_MAPPINGS.get(project_type, GUILD_MAPPINGS['custom'])
    safe_name = project_type + '_dev_guild'
    guild_file = CREWS_DIR / f"{safe_name}.yaml"
    
    if not guild_file.exists():
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
    """Run a guild to build a project using sequential LiteAgent execution."""
    from itak.lite_agent import LiteAgent
    from itak.tools.smart_edit import SmartEditTool
    from itak.tools.ripgrep import RipGrepTool
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    abs_output_dir = os.path.abspath(output_dir)
    
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
        click.secho("\n  ❌ No wizards available.", fg="red")
        return
    
    click.secho(f"\n  🚀 Starting {len(wizard_configs)}-wizard collaboration...", fg="cyan")
    click.secho(f"  📋 Project: {project_description}", fg="white")
    click.secho(f"  📁 Output: {abs_output_dir}\n", fg="white")
    
    # Tools for all wizards
    tools = [SmartEditTool(), RipGrepTool()]
    
    # Track what was created
    created_files = []
    previous_output = ""
    
    # Wizard-specific prompts to ensure file creation
    wizard_prompts = {
        'Project Manager': f"""You are the Project Manager. Plan the project structure for: {project_description}

IMPORTANT: Use the SmartEdit tool to create files. The output directory is: {abs_output_dir}

Create a project plan and then create the main HTML file:
1. Use SmartEdit with file_path="{abs_output_dir}/index.html", old_string="", new_string="<full HTML content>"
2. Plan what CSS and JS files are needed

Start by creating index.html with proper HTML5 structure.""",

        'Frontend Wizard': f"""You are the Frontend Wizard. Create the HTML structure and CSS styling for: {project_description}

Working directory: {abs_output_dir}

Previous wizard's work: {previous_output[:300] if previous_output else 'Starting fresh'}

YOUR TASK:
1. If index.html doesn't exist or is empty, use SmartEdit to create it at "{abs_output_dir}/index.html"
2. Create a CSS file at "{abs_output_dir}/styles.css" with modern, responsive styling
3. Use SmartEdit tool with file_path, old_string="", new_string="<content>"

CREATE THE FILES NOW using SmartEdit.""",

        'JavaScript Wizard': f"""You are the JavaScript Wizard. Add interactivity to: {project_description}

Working directory: {abs_output_dir}

Previous work done: {previous_output[:300] if previous_output else 'Starting fresh'}

YOUR TASK:
1. Create "{abs_output_dir}/script.js" with interactive JavaScript
2. Use SmartEdit tool: file_path="{abs_output_dir}/script.js", old_string="", new_string="<JS code>"
3. Add event listeners, DOM manipulation, modern ES6+

CREATE the JavaScript file NOW using SmartEdit.""",

        'Content Wizard': f"""You are the Content Wizard. Write compelling content for: {project_description}

Working directory: {abs_output_dir}

Previous work: {previous_output[:300] if previous_output else 'Starting fresh'}

YOUR TASK:
1. Use RipGrep to find the index.html file
2. Use SmartEdit to update content text in the HTML
3. Replace placeholder text with real, compelling copy

Update the HTML content NOW using SmartEdit.""",

        'QA Wizard': f"""You are the QA Wizard. Review the project: {project_description}

Working directory: {abs_output_dir}

YOUR TASK:
1. Use RipGrep to search for files in {abs_output_dir}
2. Check that index.html, styles.css, script.js exist
3. If any file is missing, CREATE it using SmartEdit
4. Report what files exist and any issues found

Review and fix any issues NOW.""",
    }
    
    # Run wizards sequentially
    for i, wizard_config in enumerate(wizard_configs, 1):
        wizard_name = wizard_config.get('name', 'Unknown')
        wizard_role = wizard_config.get('role', 'Developer')
        wizard_goal = wizard_config.get('goal', 'Complete the task')
        backstory = wizard_config.get('backstory', 'An expert in their field')
        llm = wizard_config.get('llm', 'ollama/qwen3-vl:2b')
        
        click.secho(f"\n  🔮 [{i}/{len(wizard_configs)}] {wizard_name} working...", fg="magenta")
        
        # Get wizard-specific prompt or fallback
        task = wizard_prompts.get(wizard_name, 
            f"Work on: {project_description}. Directory: {abs_output_dir}. Use SmartEdit to create files.")
        
        # Update prompts with previous output for later wizards
        if i > 1 and previous_output:
            task = task.replace("{previous_output[:300] if previous_output else 'Starting fresh'}", 
                               previous_output[:300])
        
        try:
            wizard_agent = LiteAgent(
                role=wizard_role,
                goal=wizard_goal,
                backstory=backstory,
                tools=tools,
                llm=llm,
                verbose=False,
                max_iterations=8,
            )
            
            result = wizard_agent.kickoff(task)
            previous_output = result.raw
            
            # Show what the wizard did
            if "SmartEdit" in previous_output or "created" in previous_output.lower():
                click.secho(f"  📝 {wizard_name} created/edited files", fg="cyan")
            
            click.secho(f"  ✓ {wizard_name} complete", fg="green")
            
        except Exception as e:
            click.secho(f"  ❌ {wizard_name} failed: {str(e)[:80]}", fg="red")
            continue
    
    # Check what was created
    click.echo()
    if os.path.exists(abs_output_dir):
        files = os.listdir(abs_output_dir)
        if files:
            click.secho(f"  ✅ Guild collaboration complete!", fg="green", bold=True)
            click.secho(f"  📁 Created files in {abs_output_dir}:", fg="cyan")
            for f in files:
                size = os.path.getsize(os.path.join(abs_output_dir, f))
                click.echo(f"      • {f} ({size} bytes)")
        else:
            click.secho(f"  ⚠️  No files were created in {abs_output_dir}", fg="yellow")
    else:
        click.secho(f"  ⚠️  Output directory was not created", fg="yellow")
    
    click.echo()
