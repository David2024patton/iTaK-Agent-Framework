"""Integrate guild system into wizard.py"""

# Read the file
with open(r'd:\test\testing\src\itak\cli\wizard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add import at top (after other imports, around line 10)
import_line = "from .guild_auto import get_or_create_guild_for_project, run_guild_build\nfrom .agent_manager import initialize_default_wizards\n"

# Find line with "from typing import Optional"
for i, line in enumerate(lines):
    if 'from typing import Optional' in line:
        # Insert imports after this line
        lines.insert(i+1, import_line)
        print(f"✅ Added imports at line {i+2}")
        break

# 2. Replace start_build function (lines 266-301) with new version
new_start_build = '''def start_build(prompt: str, output_dir: str, project_type: str = 'custom'):
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


'''

# Find start_build function and replace it
for i, line in enumerate(lines):
    if i > 260 and 'def start_build(' in line:
        # Find the end of the function (next def or end of file)
        end_idx = i + 1
        for j in range(i+1, len(lines)):
            if lines[j].startswith('def ') or lines[j].startswith('if __name__'):
                end_idx = j
                break
        
        # Replace the function
        lines[i:end_idx] = [new_start_build]
        print(f"✅ Replaced start_build function at lines {i}-{end_idx}")
        break

# 3. Update the call to start_build to include project_type
# Find where it's called (search for 'start_build(')
for i, line in enumerate(lines):
    if 'start_build(build_prompt, output_dir)' in line:
        # Add project_type parameter
        lines[i] = line.replace('start_build(build_prompt, output_dir)', 
                                'start_build(build_prompt, output_dir, project_type[1])')
        print(f"✅ Updated start_build call at line {i+1}")
        break

# Write back
with open(r'd:\test\testing\src\itak\cli\wizard.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ wizard.py updated with guild integration")
