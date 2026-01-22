"""Add initialize_default_wizards function to agent_manager.py"""

# Read the file
with open(r'd:\test\testing\src\itak\cli\agent_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 883 (after save_wizard function)
# Insert new function there

new_function = '''

def initialize_default_wizards():
    """Initialize default web dev wizards if none exist. Silent operation."""
    ensure_dirs()
    
    # Check if we already have wizards
    existing_wizards = list(AGENTS_DIR.glob('*.yaml'))
    if existing_wizards:
        return  # Already initialized
    
    # Create the 5 default web dev wizards silently
    default_wizards = [
        'project_manager', 'frontend_wizard', 'javascript_wizard', 
        'content_wizard', 'qa_wizard'
    ]
    
    for wizard_key in default_wizards:
        if wizard_key in WIZARD_TEMPLATES:
            template = WIZARD_TEMPLATES[wizard_key]
            safe_name = wizard_key
            
            agent_def = {
                'name': template['name'],
                'role': template['role'],
                'goal': template['goal'],
                'backstory': template['backstory'],
                'tools': template['tools'],
                'llm': template['llm'],
                'verbose': True,
                'allow_delegation': False,
            }
            
            agent_file = AGENTS_DIR / f"{safe_name}.yaml"
            
            with open(agent_file, 'w') as f:
                yaml.dump(agent_def, f, default_flow_style=False)


'''

# Insert after line 883 (index 883)
lines.insert(883, new_function)

# Write back
with open(r'd:\test\testing\src\itak\cli\agent_manager.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Added initialize_default_wizards() function at line 884")
