"""
iTaK AI Agent Manager
Handles agent and crew creation/management
"""
import os
import sys
import yaml
from pathlib import Path

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
RED = "\033[31m"

# Config directories
AGENTS_DIR = Path.home() / '.itak' / 'agents'
CREWS_DIR = Path.home() / '.itak' / 'crews'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_exit(value):
    """Check if user wants to exit CLI. Exits if so, returns False otherwise."""
    if value.lower() in ['/exit', 'exit', '/quit', 'quit']:
        print(f"\n{YELLOW}Goodbye!{RESET}\n")
        sys.exit(0)
    return value.lower() == '/back'


def ensure_dirs():
    """Ensure config directories exist."""
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CREWS_DIR.mkdir(parents=True, exist_ok=True)


def print_agent_menu():
    """Print the Wizards & Guilds submenu."""
    clear_screen()
    ensure_dirs()
    
    # Count existing wizards and guilds
    wizards = list(AGENTS_DIR.glob('*.yaml'))
    guilds = list(CREWS_DIR.glob('*.yaml'))
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🔮 Wizards & Guilds                                         ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Build and manage your magical workforce                   │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    🧙 Wizards → Specialized AI with custom roles/powers       │\033[0m")
    print(f"  \033[90m│    🏰 Guilds  → Teams of wizards working together             │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    print(f"  {BOLD}Wizards:{RESET} {len(wizards)} saved  |  {BOLD}Guilds:{RESET} {len(guilds)} saved")
    print()
    
    print(f"  {GREEN}[1]{RESET} 🧙 {WHITE}Create Wizard{RESET}     {DIM}Define a new specialized wizard{RESET}")
    print(f"  {GREEN}[2]{RESET} 🏰 {WHITE}Create Guild{RESET}      {DIM}Build a team of wizards{RESET}")
    print()
    print(f"  {GREEN}[3]{RESET} 📋 {WHITE}List Wizards{RESET}      {DIM}View and manage wizards{RESET}")
    print(f"  {GREEN}[4]{RESET} 📋 {WHITE}List Guilds{RESET}       {DIM}View and manage guilds{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()

# Pre-built wizard templates
WIZARD_TEMPLATES = {
    'coder': {
        'name': 'Code Wizard',
        'role': 'Senior Software Developer',
        'goal': 'Write clean, efficient, well-documented code',
        'backstory': 'An experienced developer with mastery of multiple languages and best practices',
        'tools': ['file_read', 'file_write', 'code_search', 'shell'],
        'llm': 'ollama/qwen3-vl:2b'
    },
    'researcher': {
        'name': 'Research Wizard',
        'role': 'Web Research Specialist',
        'goal': 'Find accurate, comprehensive information online',
        'backstory': 'A meticulous researcher skilled at finding reliable sources',
        'tools': ['web_search', 'file_write'],
        'llm': 'ollama/qwen3:4b'
    },
    'writer': {
        'name': 'Writer Wizard',
        'role': 'Content Writer',
        'goal': 'Create compelling, well-structured content',
        'backstory': 'A creative writer with expertise in various formats',
        'tools': ['file_read', 'file_write'],
        'llm': 'ollama/qwen3:4b'
    },
    'analyst': {
        'name': 'Data Wizard',
        'role': 'Data Analyst',
        'goal': 'Analyze data and provide insights',
        'backstory': 'An expert at finding patterns and extracting meaning from data',
        'tools': ['file_read', 'code_search', 'shell'],
        'llm': 'ollama/qwen3:4b'
    },
}


def create_agent():
    """Wizard to create a new wizard (agent) - with mode selection."""
    import click
    import sys
    
    clear_screen()
    
    # Themed header
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🧙 Create New Wizard                                        ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Choose how you want to create your wizard                 │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    # Mode selection
    print(f"  {GREEN}[1]{RESET} 🤖 {WHITE}AI-Assisted{RESET}     {DIM}Describe what you need, AI designs it{RESET}")
    print(f"  {GREEN}[2]{RESET} 📝 {WHITE}Manual{RESET}          {DIM}Define everything step-by-step{RESET}")
    print(f"  {GREEN}[3]{RESET} 📋 {WHITE}Templates{RESET}       {DIM}Start from a pre-built wizard{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()
    
    try:
        choice = click.prompt(click.style("  Select", fg="cyan"), default="0", show_default=False).strip()
        
        check_exit(choice)  # Will exit CLI if user typed exit
        if choice == '0' or choice == '':
            return
        
        if choice == '1':
            create_wizard_ai_assisted()
        elif choice == '2':
            create_wizard_manual()
        elif choice == '3':
            create_wizard_from_template()
            
    except (KeyboardInterrupt, click.Abort):
        pass


def create_wizard_ai_assisted():
    """AI-assisted wizard creation using Ollama."""
    import click
    import json
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🤖 AI-Assisted Wizard Creation                              ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  {DIM}Describe the wizard you want to create and AI will design it{RESET}")
    print(f"  {DIM}Example: 'A Python developer who can write and test code'{RESET}")
    print()
    
    try:
        description = click.prompt(click.style("  Describe your wizard", fg="cyan"), default="", show_default=False).strip()
        
        if not description or description.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            input("\n  Press Enter to continue...")
            return
        
        print(f"\n  {DIM}🔮 Generating wizard configuration...{RESET}")
        
        # Generate using Ollama
        try:
            import ollama
            
            prompt = f"""Based on this description, create a wizard configuration:
"{description}"

Respond ONLY with valid JSON in this exact format:
{{"name": "Wizard Name", "role": "Role Title", "goal": "Primary goal", "tools": ["file_read", "file_write"]}}

Available tools: file_read, file_write, code_search, web_search, shell
Keep the response short. Only output the JSON, nothing else."""

            response = ollama.chat(model='qwen3-vl:2b', messages=[
                {'role': 'user', 'content': prompt}
            ], options={'temperature': 0.3})
            
            # Extract JSON from response
            content = response['message']['content']
            
            # Find JSON in response
            import re
            json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
            if json_match:
                wizard_config = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
            
            # Show preview
            clear_screen()
            print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
            print(f"  \033[35m║  🔮 AI Generated Wizard                                      ║\033[0m")
            print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
            print()
            
            name = wizard_config.get('name', 'AI Wizard')
            role = wizard_config.get('role', 'AI Assistant')
            goal = wizard_config.get('goal', 'Help with tasks')
            tools = wizard_config.get('tools', ['file_read', 'file_write'])
            
            print(f"  {BOLD}Name:{RESET}    {CYAN}{name}{RESET}")
            print(f"  {BOLD}Role:{RESET}    {role}")
            print(f"  {BOLD}Mission:{RESET} {goal}")
            print(f"  {BOLD}Powers:{RESET}  {', '.join(tools)}")
            print(f"  {BOLD}Brain:{RESET}   ollama/qwen3-vl:2b")
            print()
            
            confirm = click.prompt(click.style("  Create this wizard? [Y/n]", fg="cyan"), default="y", show_default=False).strip().lower()
            
            if confirm in ['y', 'yes', '']:
                save_wizard(name, role, goal, tools, 'ollama/qwen3-vl:2b')
            else:
                print(f"\n  {YELLOW}Cancelled{RESET}")
                input("\n  Press Enter to continue...")
                
        except Exception as e:
            print(f"\n  {RED}AI generation failed: {e}{RESET}")
            print(f"  {DIM}Falling back to manual mode...{RESET}")
            input("\n  Press Enter to continue...")
            create_wizard_manual()
            
    except (KeyboardInterrupt, click.Abort):
        pass


def create_wizard_from_template():
    """Create wizard from pre-built template with full customization."""
    import click
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  📋 Wizard Templates                                         ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  {DIM}Choose a pre-built wizard template to customize{RESET}")
    print()
    
    templates = list(WIZARD_TEMPLATES.items())
    for i, (key, template) in enumerate(templates, 1):
        print(f"  {GREEN}[{i}]{RESET} {template['name']}")
        print(f"      {DIM}{template['role']} • {template['goal'][:40]}...{RESET}")
        print()
    
    print(f"  {GREEN}[0]{RESET} ↩️  Back")
    print()
    
    try:
        choice = click.prompt(click.style("  Select template", fg="cyan"), default="0", show_default=False).strip()
        
        if choice.lower() in ['/exit', 'exit', '0', '']:
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                key, template = templates[idx]
                
                # Show customization screen
                clear_screen()
                print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
                print(f"  \033[35m║  ✏️  Customize Template: {template['name']:<34} ║\033[0m")
                print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
                print()
                
                print(f"  {DIM}Press Enter to keep defaults, or type to change{RESET}")
                print(f"  {DIM}Type /exit to cancel{RESET}")
                print()
                
                # Name
                print(f"  {BOLD}Name{RESET} {DIM}(current: {template['name']}){RESET}")
                name = click.prompt(click.style("  Name", fg="cyan"), default=template['name'], show_default=False).strip()
                if name.lower() in ['/exit', 'exit']:
                    return
                print(f"  {GREEN}✓{RESET} {name}\n")
                
                # Role
                print(f"  {BOLD}Role{RESET} {DIM}(current: {template['role']}){RESET}")
                role = click.prompt(click.style("  Role", fg="cyan"), default=template['role'], show_default=False).strip()
                if role.lower() in ['/exit', 'exit']:
                    return
                print(f"  {GREEN}✓{RESET} {role}\n")
                
                # Goal/Mission
                print(f"  {BOLD}Mission{RESET} {DIM}(current: {template['goal']}){RESET}")
                goal = click.prompt(click.style("  Mission", fg="cyan"), default=template['goal'], show_default=False).strip()
                if goal.lower() in ['/exit', 'exit']:
                    return
                print(f"  {GREEN}✓{RESET} {goal}\n")
                
                # Powers - show current and allow change
                available_tools = [
                    ('📖 file_read', 'file_read'),
                    ('✍️ file_write', 'file_write'),
                    ('🔍 code_search', 'code_search'),
                    ('🌐 web_search', 'web_search'),
                    ('⚡ shell', 'shell'),
                ]
                
                # Convert current tools to numbers
                current_nums = []
                for t in template['tools']:
                    for i, (_, tool_id) in enumerate(available_tools, 1):
                        if t == tool_id:
                            current_nums.append(str(i))
                default_powers = ','.join(current_nums)
                
                print(f"  {BOLD}Powers{RESET} {DIM}(current: {', '.join(template['tools'])}){RESET}")
                for i, (display, _) in enumerate(available_tools, 1):
                    marker = "●" if str(i) in current_nums else "○"
                    print(f"    [{CYAN}{i}{RESET}] {marker} {display}")
                
                tool_input = click.prompt(click.style("  Powers", fg="cyan"), default=default_powers, show_default=False).strip()
                if tool_input.lower() in ['/exit', 'exit']:
                    return
                
                selected_tools = []
                for num in tool_input.split(','):
                    try:
                        i = int(num.strip()) - 1
                        if 0 <= i < len(available_tools):
                            selected_tools.append(available_tools[i][1])
                    except:
                        pass
                if not selected_tools:
                    selected_tools = template['tools']
                print(f"  {GREEN}✓{RESET} {len(selected_tools)} powers\n")
                
                # Model/Brain
                print(f"  {BOLD}Brain{RESET} {DIM}(current: {template['llm']}){RESET}")
                llm = click.prompt(click.style("  Model", fg="cyan"), default=template['llm'], show_default=False).strip()
                if llm.lower() in ['/exit', 'exit']:
                    return
                print(f"  {GREEN}✓{RESET} {llm}\n")
                
                # Save wizard
                save_wizard(name, role, goal, selected_tools, llm)
                
            else:
                print(f"\n  {YELLOW}Invalid selection{RESET}")
                input("\n  Press Enter to continue...")
        except ValueError:
            print(f"\n  {YELLOW}Invalid selection{RESET}")
            input("\n  Press Enter to continue...")
            
    except (KeyboardInterrupt, click.Abort):
        pass


def create_wizard_manual():
    """Manual step-by-step wizard creation."""
    import click
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  📝 Manual Wizard Creation                                   ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  {DIM}Define your wizard step-by-step. Type /exit to cancel.{RESET}")
    print()
    
    try:
        # Step 1: Name
        print(f"  {BOLD}Step 1 of 5: Wizard Name{RESET}")
        name = click.prompt(click.style("  Name", fg="cyan"), default="", show_default=False).strip()
        if not name or name.lower() in ['/exit', 'exit']:
            return
        print(f"  {GREEN}✓{RESET} {name}\n")
        
        # Step 2: Role
        print(f"  {BOLD}Step 2 of 5: Role{RESET}")
        role = click.prompt(click.style("  Role", fg="cyan"), default="AI Assistant", show_default=False).strip()
        if role.lower() in ['/exit', 'exit']:
            return
        print(f"  {GREEN}✓{RESET} {role}\n")
        
        # Step 3: Goal
        print(f"  {BOLD}Step 3 of 5: Mission{RESET}")
        goal = click.prompt(click.style("  Mission", fg="cyan"), default="Help with tasks", show_default=False).strip()
        if goal.lower() in ['/exit', 'exit']:
            return
        print(f"  {GREEN}✓{RESET} {goal}\n")
        
        # Step 4: Powers
        print(f"  {BOLD}Step 4 of 5: Powers{RESET}")
        available_tools = [
            ('📖 file_read', 'file_read'),
            ('✍️ file_write', 'file_write'),
            ('🔍 code_search', 'code_search'),
            ('🌐 web_search', 'web_search'),
            ('⚡ shell', 'shell'),
        ]
        for i, (display, _) in enumerate(available_tools, 1):
            print(f"    [{CYAN}{i}{RESET}] {display}")
        
        tool_input = click.prompt(click.style("  Powers (1,2,3)", fg="cyan"), default="1,2,3", show_default=False).strip()
        if tool_input.lower() in ['/exit', 'exit']:
            return
        
        selected_tools = []
        for num in tool_input.split(','):
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_tools):
                    selected_tools.append(available_tools[idx][1])
            except:
                pass
        if not selected_tools:
            selected_tools = ['file_read', 'file_write']
        print(f"  {GREEN}✓{RESET} {len(selected_tools)} powers\n")
        
        # Step 5: Model
        print(f"  {BOLD}Step 5 of 5: Brain{RESET}")
        llm = click.prompt(click.style("  Model", fg="cyan"), default="ollama/qwen3-vl:2b", show_default=False).strip()
        if llm.lower() in ['/exit', 'exit']:
            return
        print(f"  {GREEN}✓{RESET} {llm}\n")
        
        save_wizard(name, role, goal, selected_tools, llm)
        
    except (KeyboardInterrupt, click.Abort):
        pass


def save_wizard(name, role, goal, tools, llm):
    """Save wizard to YAML file."""
    safe_name = name.lower().replace(' ', '_').replace('-', '_')
    
    agent_def = {
        'name': name,
        'role': role,
        'goal': goal,
        'backstory': f"A skilled {role} wizard with expertise in their craft",
        'tools': tools,
        'llm': llm,
        'verbose': True,
        'allow_delegation': False,
    }
    
    ensure_dirs()
    agent_file = AGENTS_DIR / f"{safe_name}.yaml"
    
    with open(agent_file, 'w') as f:
        yaml.dump(agent_def, f, default_flow_style=False)
    
    # Success screen
    clear_screen()
    print(f"\n  \033[32m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[32m║  ✓ Wizard Created!                                           ║\033[0m")
    print(f"  \033[32m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    print(f"  {BOLD}Name:{RESET}    {CYAN}{name}{RESET}")
    print(f"  {BOLD}Role:{RESET}    {role}")
    print(f"  {BOLD}Mission:{RESET} {goal}")
    print(f"  {BOLD}Powers:{RESET}  {', '.join(tools)}")
    print(f"  {BOLD}Brain:{RESET}   {llm}")
    print()
    print(f"  {DIM}Saved to: {agent_file}{RESET}")
    
    input("\n  Press Enter to continue...")




# Pre-built guild templates with example compositions
GUILD_TEMPLATES = {
    'web_dev': {
        'name': 'Web Dev Guild',
        'description': 'Full-stack web development team',
        'recommended_wizards': ['coder', 'researcher', 'writer'],
        'workflow': 'sequential'
    },
    'research': {
        'name': 'Research Guild',
        'description': 'Deep research and analysis team',
        'recommended_wizards': ['researcher', 'analyst', 'writer'],
        'workflow': 'sequential'
    },
    'content': {
        'name': 'Content Guild',
        'description': 'Content creation and writing team',
        'recommended_wizards': ['writer', 'researcher'],
        'workflow': 'sequential'
    },
    'automation': {
        'name': 'Automation Guild',
        'description': 'Script and automation team',
        'recommended_wizards': ['coder', 'analyst'],
        'workflow': 'sequential'
    },
}


def create_crew():
    """Create a new Guild (team of wizards) with mode selection."""
    import click
    
    clear_screen()
    
    # Themed header
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🏰 Create New Guild                                         ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Choose how you want to create your guild                  │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    # Mode selection
    print(f"  {GREEN}[1]{RESET} 🤖 {WHITE}AI-Assisted{RESET}     {DIM}Describe your project, AI picks the team{RESET}")
    print(f"  {GREEN}[2]{RESET} 📝 {WHITE}Manual{RESET}          {DIM}Select wizards yourself{RESET}")
    print(f"  {GREEN}[3]{RESET} 📋 {WHITE}Templates{RESET}       {DIM}Start from a pre-built guild{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()
    
    try:
        choice = click.prompt(click.style("  Select", fg="cyan"), default="0", show_default=False).strip()
        
        check_exit(choice)
        if choice == '0' or choice == '':
            return
        
        if choice == '1':
            create_guild_ai_assisted()
        elif choice == '2':
            create_guild_manual()
        elif choice == '3':
            create_guild_from_template()
            
    except (KeyboardInterrupt, click.Abort):
        pass


def create_guild_ai_assisted():
    """AI-assisted guild creation - AI picks wizards based on task description."""
    import click
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🤖 AI-Assisted Guild Creation                               ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    # Check for existing wizards
    agents = list(AGENTS_DIR.glob('*.yaml'))
    
    if not agents:
        print(f"  {YELLOW}⚠️  No wizards created yet.{RESET}")
        print(f"  {DIM}Create some wizards first at Wizards → Create Wizard.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    # Load wizard info
    wizard_info = []
    for agent_file in agents:
        try:
            with open(agent_file) as f:
                agent = yaml.safe_load(f)
            wizard_info.append({
                'id': agent_file.stem,
                'name': agent.get('name', agent_file.stem),
                'role': agent.get('role', 'N/A'),
                'tools': agent.get('tools', [])
            })
        except:
            pass
    
    if not wizard_info:
        print(f"  {YELLOW}No valid wizards found.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    # Show available wizards
    print(f"  {DIM}Available Wizards:{RESET}")
    for w in wizard_info:
        print(f"    🧙 {w['name']} ({w['role']})")
        print(f"       {DIM}Tools: {', '.join(w['tools'])}{RESET}")
    print()
    
    print(f"  {DIM}Type /exit to cancel{RESET}")
    print()
    
    try:
        # Get project description
        print(f"  {BOLD}What are you building?{RESET}")
        print(f"  {DIM}Example: 'A web scraper that saves data to CSV'{RESET}")
        description = click.prompt(click.style("  Project", fg="cyan"), default="", show_default=False).strip()
        
        check_exit(description)
        if not description:
            return
        
        print(f"\n  {MAGENTA}✦{RESET} {DIM}Analyzing wizards for your project...{RESET}")
        
        # Build prompt for AI
        wizard_list = "\n".join([
            f"- {w['id']}: {w['name']} (Role: {w['role']}, Tools: {', '.join(w['tools'])})"
            for w in wizard_info
        ])
        
        prompt = f"""You are an AI team coordinator. Given a project description and available wizards, select the best team.

PROJECT: {description}

AVAILABLE WIZARDS:
{wizard_list}

Select 2-4 wizards that would work best together for this project.
Respond with ONLY a JSON object like this:
{{"guild_name": "Name for the team", "wizards": ["wizard_id1", "wizard_id2"], "workflow": "sequential", "reasoning": "Brief explanation"}}

Choose "sequential" for step-by-step work or "hierarchical" for managed teamwork.
Only include wizard IDs that exist in the list above."""

        try:
            import ollama
            response = ollama.chat(model='qwen3-vl:2b', messages=[
                {'role': 'user', 'content': prompt}
            ], options={'temperature': 0.3})
            
            response_text = response['message']['content']
            
            # Parse JSON from response
            import json
            import re
            json_match = re.search(r'\{[^{}]+\}', response_text.replace('\n', ' '))
            
            if json_match:
                result = json.loads(json_match.group())
                
                guild_name = result.get('guild_name', 'AI Guild')
                selected_ids = result.get('wizards', [])
                workflow = result.get('workflow', 'sequential')
                reasoning = result.get('reasoning', '')
                
                # Validate selected wizards exist
                valid_ids = [w['id'] for w in wizard_info]
                selected_ids = [w for w in selected_ids if w in valid_ids]
                
                if not selected_ids:
                    print(f"  {YELLOW}AI couldn't find matching wizards. Try manual mode.{RESET}")
                    input("\n  Press Enter to continue...")
                    return
                
                # Show recommendation
                clear_screen()
                print(f"\n  \033[32m╔══════════════════════════════════════════════════════════════╗\033[0m")
                print(f"  \033[32m║  ✦ AI Recommendation                                         ║\033[0m")
                print(f"  \033[32m╚══════════════════════════════════════════════════════════════╝\033[0m")
                print()
                
                print(f"  {BOLD}Guild:{RESET}    {CYAN}{guild_name}{RESET}")
                print(f"  {BOLD}Workflow:{RESET} {'👑 Hierarchical' if workflow == 'hierarchical' else '➡️ Sequential'}")
                print()
                print(f"  {BOLD}Team Composition:{RESET}")
                for wid in selected_ids:
                    w = next((x for x in wizard_info if x['id'] == wid), None)
                    if w:
                        print(f"    🧙 {w['name']} - {w['role']}")
                print()
                
                if reasoning:
                    print(f"  {DIM}Reasoning: {reasoning}{RESET}")
                    print()
                
                confirm = click.prompt(click.style("  Create this guild? [Y/n]", fg="cyan"), default="y", show_default=False).strip().lower()
                
                if confirm in ['y', 'yes', '']:
                    # Save guild
                    safe_name = guild_name.lower().replace(' ', '_').replace('-', '_')
                    crew_def = {
                        'name': guild_name,
                        'agents': selected_ids,
                        'workflow': workflow,
                        'verbose': False,
                    }
                    
                    ensure_dirs()
                    crew_file = CREWS_DIR / f"{safe_name}.yaml"
                    
                    with open(crew_file, 'w') as f:
                        yaml.dump(crew_def, f, default_flow_style=False)
                    
                    print(f"\n  {GREEN}✓ Guild '{guild_name}' created!{RESET}")
                    print(f"  {DIM}Saved to: {crew_file}{RESET}")
                else:
                    print(f"\n  {YELLOW}Cancelled{RESET}")
            else:
                print(f"  {YELLOW}Couldn't parse AI response. Try manual mode.{RESET}")
                
        except Exception as e:
            print(f"  {RED}Error: {e}{RESET}")
            print(f"  {DIM}Make sure Ollama is running{RESET}")
            
    except (KeyboardInterrupt, click.Abort):
        print(f"\n  {DIM}Cancelled{RESET}")
    
    input("\n  Press Enter to continue...")


def create_guild_from_template():
    """Create guild from pre-built template."""
    import click
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  📋 Guild Templates                                          ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    templates = list(GUILD_TEMPLATES.items())
    
    for i, (key, template) in enumerate(templates, 1):
        print(f"  {GREEN}[{i}]{RESET} 🏰 {WHITE}{template['name']}{RESET}")
        print(f"      {DIM}{template['description']}{RESET}")
        print(f"      {DIM}Needs: {', '.join(template['recommended_wizards'])}{RESET}")
        print()
    
    print(f"  {GREEN}[0]{RESET} ↩️  Back")
    print()
    
    try:
        choice = click.prompt(click.style("  Select template", fg="cyan"), default="0", show_default=False).strip()
        
        check_exit(choice)
        if choice == '0' or choice == '':
            return
        
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(templates):
                return
        except ValueError:
            return
        
        key, template = templates[idx]
        
        # Check if required wizards exist
        agents = list(AGENTS_DIR.glob('*.yaml'))
        existing_ids = [a.stem for a in agents]
        
        # Find matching wizards
        matched = []
        for rec in template['recommended_wizards']:
            # Try to find a wizard that matches the recommended type
            for agent_file in agents:
                if rec in agent_file.stem.lower():
                    matched.append(agent_file.stem)
                    break
        
        if not matched:
            print(f"\n  {YELLOW}⚠️  No matching wizards found.{RESET}")
            print(f"  {DIM}Create wizards with names containing: {', '.join(template['recommended_wizards'])}{RESET}")
            input("\n  Press Enter to continue...")
            return
        
        # Get custom name
        print(f"\n  {BOLD}Guild Name{RESET}")
        name = click.prompt(click.style("  Name", fg="cyan"), default=template['name'], show_default=False).strip()
        check_exit(name)
        
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        
        # Save
        crew_def = {
            'name': name,
            'agents': matched,
            'workflow': template['workflow'],
            'verbose': False,
        }
        
        ensure_dirs()
        crew_file = CREWS_DIR / f"{safe_name}.yaml"
        
        with open(crew_file, 'w') as f:
            yaml.dump(crew_def, f, default_flow_style=False)
        
        print(f"\n  {GREEN}✓ Guild '{name}' created with {len(matched)} wizard(s)!{RESET}")
        print(f"  {DIM}Wizards: {', '.join(matched)}{RESET}")
        
    except (KeyboardInterrupt, click.Abort):
        pass
    
    input("\n  Press Enter to continue...")


def create_guild_manual():
    """Manual guild creation - user selects wizards themselves."""
    import click
    
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  📝 Manual Guild Creation                                    ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    # Check for existing wizards
    agents = list(AGENTS_DIR.glob('*.yaml'))
    
    if not agents:
        print(f"  {YELLOW}⚠️  No wizards created yet.{RESET}")
        print(f"  {DIM}Create some wizards first at Wizards → Create Wizard.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    print(f"  {DIM}Found {len(agents)} wizard(s) available{RESET}")
    print(f"  {DIM}Type /exit to cancel{RESET}")
    print()
    
    try:
        # Step 1: Guild name
        print(f"  {BOLD}Step 1 of 3: Guild Name{RESET}")
        print(f"  {DIM}Give your team an epic name{RESET}")
        name = click.prompt(click.style("  Name", fg="cyan"), default="", show_default=False).strip()
        
        check_exit(name)
        if not name:
            print(f"  {YELLOW}Cancelled{RESET}")
            input("\n  Press Enter to continue...")
            return
        
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        print(f"  {GREEN}✓{RESET} {name}\n")
        
        # Step 2: Select wizards
        print(f"  {BOLD}Step 2 of 3: Recruit Wizards{RESET}")
        print(f"  {DIM}Choose which wizards join this guild{RESET}")
        print()
        
        for i, agent_file in enumerate(agents, 1):
            try:
                with open(agent_file) as f:
                    agent = yaml.safe_load(f)
                print(f"    [{CYAN}{i}{RESET}] 🧙 {agent.get('name', agent_file.stem)}")
                print(f"        {DIM}{agent.get('role', 'N/A')}{RESET}")
            except:
                print(f"    [{CYAN}{i}{RESET}] {agent_file.stem}")
        
        print()
        print(f"  {DIM}Enter numbers separated by commas (e.g., 1,2,3){RESET}")
        agent_input = click.prompt(click.style("  Wizards", fg="cyan"), default="", show_default=False).strip()
        
        check_exit(agent_input)
        
        selected_agents = []
        try:
            for num in agent_input.split(','):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(agents):
                    selected_agents.append(agents[idx].stem)
        except:
            pass
        
        if not selected_agents:
            print(f"  {YELLOW}No wizards selected{RESET}")
            input("\n  Press Enter to continue...")
            return
        
        print(f"  {GREEN}✓{RESET} {len(selected_agents)} wizard(s) recruited\n")
        
        # Step 3: Workflow type
        print(f"  {BOLD}Step 3 of 3: Workflow Style{RESET}")
        print(f"  {DIM}How should the wizards coordinate?{RESET}")
        print()
        print(f"    [{CYAN}1{RESET}] ➡️  Sequential   {DIM}Wizards work one after another{RESET}")
        print(f"    [{CYAN}2{RESET}] 👑 Hierarchical {DIM}Leader assigns tasks to wizards{RESET}")
        print()
        
        workflow = click.prompt(click.style("  Style", fg="cyan"), default="1", show_default=False).strip()
        check_exit(workflow)
        workflow_type = "hierarchical" if workflow == "2" else "sequential"
        workflow_emoji = "👑" if workflow == "2" else "➡️"
        print(f"  {GREEN}✓{RESET} {workflow_emoji} {workflow_type.capitalize()}\n")
        
        # Build guild definition
        crew_def = {
            'name': name,
            'agents': selected_agents,
            'workflow': workflow_type,
            'verbose': False,
        }
        
        # Save to file
        ensure_dirs()
        crew_file = CREWS_DIR / f"{safe_name}.yaml"
        
        with open(crew_file, 'w') as f:
            yaml.dump(crew_def, f, default_flow_style=False)
        
        # Success message
        clear_screen()
        print(f"\n  \033[32m╔══════════════════════════════════════════════════════════════╗\033[0m")
        print(f"  \033[32m║  ✓ Guild Created!                                            ║\033[0m")
        print(f"  \033[32m╚══════════════════════════════════════════════════════════════╝\033[0m")
        print()
        print(f"  {BOLD}Name:{RESET}     {CYAN}{name}{RESET}")
        print(f"  {BOLD}Wizards:{RESET}  {', '.join(selected_agents)}")
        print(f"  {BOLD}Workflow:{RESET} {workflow_emoji} {workflow_type.capitalize()}")
        print()
        print(f"  {DIM}Saved to: {crew_file}{RESET}")
        
    except (KeyboardInterrupt, click.Abort):
        print(f"\n\n  {DIM}Cancelled{RESET}")
    
    input("\n  Press Enter to continue...")



def list_agents():
    """List and manage wizards with edit/delete options."""
    import click
    
    while True:
        clear_screen()
        
        print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
        print(f"  \033[35m║  📋 Manage Wizards                                           ║\033[0m")
        print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
        print()
        
        agents = list(AGENTS_DIR.glob('*.yaml'))
        
        if not agents:
            print(f"  {DIM}No wizards created yet.{RESET}")
            print(f"  {DIM}Use Create Wizard to build one.{RESET}")
            input("\n  Press Enter to go back...")
            return
        
        # List all wizards
        wizard_data = []
        for i, agent_file in enumerate(agents, 1):
            try:
                with open(agent_file) as f:
                    agent = yaml.safe_load(f)
                wizard_data.append((agent_file, agent))
                print(f"  {GREEN}[{i}]{RESET} 🧙 {CYAN}{agent.get('name', agent_file.stem)}{RESET}")
                print(f"      {DIM}Role: {agent.get('role', 'N/A')}{RESET}")
                print(f"      {DIM}Powers: {', '.join(agent.get('tools', []))}{RESET}")
                print()
            except:
                wizard_data.append((agent_file, None))
                print(f"  [{i}] {agent_file.stem} {YELLOW}(error reading){RESET}")
                print()
        
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        print(f"  {DIM}Select a wizard to view/edit/delete{RESET}")
        print()
        
        try:
            choice = click.prompt(click.style("  Select wizard", fg="cyan"), default="0", show_default=False).strip()
            
            check_exit(choice)
            if choice == '0' or choice == '':
                return
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(wizard_data):
                    agent_file, agent = wizard_data[idx]
                    if agent:
                        # Show wizard details with actions
                        manage_wizard(agent_file, agent)
            except ValueError:
                pass
                
        except (KeyboardInterrupt, click.Abort):
            return


def manage_wizard(agent_file, agent):
    """Manage a single wizard - view, edit, delete."""
    import click
    
    while True:
        clear_screen()
        
        name = agent.get('name', agent_file.stem)
        role = agent.get('role', 'N/A')
        goal = agent.get('goal', 'N/A')
        tools = agent.get('tools', [])
        llm = agent.get('llm', 'ollama/qwen3:4b')
        
        print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
        print(f"  \033[35m║  🧙 {name:<56} ║\033[0m")
        print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
        print()
        
        print(f"  {BOLD}Role:{RESET}    {role}")
        print(f"  {BOLD}Mission:{RESET} {goal}")
        print(f"  {BOLD}Powers:{RESET}  {', '.join(tools) if tools else 'None'}")
        print(f"  {BOLD}Brain:{RESET}   {llm}")
        print()
        print(f"  {DIM}File: {agent_file}{RESET}")
        print()
        
        print(f"  {GREEN}[1]{RESET} ✏️  {WHITE}Edit{RESET}       {DIM}Modify this wizard{RESET}")
        print(f"  {GREEN}[2]{RESET} 🗑️  {WHITE}Delete{RESET}     {DIM}Remove this wizard{RESET}")
        print()
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Action", fg="cyan"), default="0", show_default=False).strip()
            
            check_exit(choice)
            if choice == '0' or choice == '':
                return
            
            if choice == '1':
                # Edit wizard
                edit_wizard(agent_file, agent)
                # Reload agent data after edit
                try:
                    with open(agent_file) as f:
                        agent = yaml.safe_load(f)
                except:
                    return
                    
            elif choice == '2':
                # Delete wizard
                confirm = click.prompt(
                    click.style(f"  Type '{name}' to confirm delete", fg="red"),
                    default=""
                ).strip()
                
                if confirm == name:
                    agent_file.unlink()
                    print(f"\n  {GREEN}✓ Wizard deleted{RESET}")
                    input("\n  Press Enter to continue...")
                    return
                else:
                    print(f"\n  {YELLOW}Cancelled - name didn't match{RESET}")
                    input("\n  Press Enter to continue...")
                    
        except (KeyboardInterrupt, click.Abort):
            return


def edit_wizard(agent_file, agent):
    """Edit an existing wizard."""
    import click
    
    clear_screen()
    
    name = agent.get('name', agent_file.stem)
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  ✏️  Edit Wizard: {name:<42} ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  {DIM}Press Enter to keep current value, or type new value{RESET}")
    print(f"  {DIM}Type /exit to cancel{RESET}")
    print()
    
    try:
        # Name
        print(f"  {BOLD}Name{RESET} {DIM}(current: {agent.get('name', 'N/A')}){RESET}")
        new_name = click.prompt(click.style("  Name", fg="cyan"), default=agent.get('name', ''), show_default=False).strip()
        if check_exit(new_name):
            return
        if new_name:
            agent['name'] = new_name
        print(f"  {GREEN}✓{RESET}\n")
        
        # Role
        print(f"  {BOLD}Role{RESET} {DIM}(current: {agent.get('role', 'N/A')}){RESET}")
        new_role = click.prompt(click.style("  Role", fg="cyan"), default=agent.get('role', ''), show_default=False).strip()
        if check_exit(new_role):
            return
        if new_role:
            agent['role'] = new_role
        print(f"  {GREEN}✓{RESET}\n")
        
        # Goal
        print(f"  {BOLD}Mission{RESET} {DIM}(current: {agent.get('goal', 'N/A')}){RESET}")
        new_goal = click.prompt(click.style("  Mission", fg="cyan"), default=agent.get('goal', ''), show_default=False).strip()
        if check_exit(new_goal):
            return
        if new_goal:
            agent['goal'] = new_goal
        print(f"  {GREEN}✓{RESET}\n")
        
        # Tools
        available_tools = [
            ('📖 file_read', 'file_read'),
            ('✍️ file_write', 'file_write'),
            ('🔍 code_search', 'code_search'),
            ('🌐 web_search', 'web_search'),
            ('⚡ shell', 'shell'),
        ]
        
        current_tools = agent.get('tools', [])
        current_nums = []
        for t in current_tools:
            for i, (_, tool_id) in enumerate(available_tools, 1):
                if t == tool_id:
                    current_nums.append(str(i))
        default_powers = ','.join(current_nums)
        
        print(f"  {BOLD}Powers{RESET} {DIM}(current: {', '.join(current_tools)}){RESET}")
        for i, (display, _) in enumerate(available_tools, 1):
            marker = "●" if str(i) in current_nums else "○"
            print(f"    [{CYAN}{i}{RESET}] {marker} {display}")
        
        tool_input = click.prompt(click.style("  Powers", fg="cyan"), default=default_powers, show_default=False).strip()
        if check_exit(tool_input):
            return
        
        selected_tools = []
        for num in tool_input.split(','):
            try:
                i = int(num.strip()) - 1
                if 0 <= i < len(available_tools):
                    selected_tools.append(available_tools[i][1])
            except:
                pass
        if selected_tools:
            agent['tools'] = selected_tools
        print(f"  {GREEN}✓{RESET}\n")
        
        # LLM
        print(f"  {BOLD}Brain{RESET} {DIM}(current: {agent.get('llm', 'ollama/qwen3:4b')}){RESET}")
        new_llm = click.prompt(click.style("  Model", fg="cyan"), default=agent.get('llm', 'ollama/qwen3:4b'), show_default=False).strip()
        if check_exit(new_llm):
            return
        if new_llm:
            agent['llm'] = new_llm
        print(f"  {GREEN}✓{RESET}\n")
        
        # Save
        with open(agent_file, 'w') as f:
            yaml.dump(agent, f, default_flow_style=False)
        
        print(f"  {GREEN}✓ Wizard updated!{RESET}")
        input("\n  Press Enter to continue...")
        
    except (KeyboardInterrupt, click.Abort):
        pass


def list_crews():
    """List and manage crews."""
    import click
    
    while True:
        clear_screen()
        print(f"\n  {BOLD}{MAGENTA}📋 Saved Crews{RESET}\n")
        
        crews = list(CREWS_DIR.glob('*.yaml'))
        
        if not crews:
            print(f"  {DIM}No crews defined yet.{RESET}")
            print(f"  {DIM}Use 'Create Crew' to build one.{RESET}")
            input("\n  Press Enter to go back...")
            return
        
        for i, crew_file in enumerate(crews, 1):
            try:
                with open(crew_file) as f:
                    crew = yaml.safe_load(f)
                print(f"  [{i}] {CYAN}{crew.get('name', crew_file.stem)}{RESET}")
                print(f"      {DIM}Agents: {', '.join(crew.get('agents', []))}{RESET}")
                print(f"      {DIM}Workflow: {crew.get('workflow', 'sequential')}{RESET}")
            except:
                print(f"  [{i}] {crew_file.stem} {YELLOW}(error reading){RESET}")
        
        print(f"\n  {DIM}Enter number to delete, or 0 to go back{RESET}")
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if choice == '0' or choice == '':
                return
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(crews):
                    crew_file = crews[idx]
                    confirm = click.prompt(
                        click.style(f"  Delete {crew_file.stem}? (y/N)", fg="yellow"),
                        default="n"
                    ).strip().lower()
                    
                    if confirm == 'y':
                        crew_file.unlink()
                        print(f"  {GREEN}✅ Deleted{RESET}")
            except ValueError:
                pass
                
        except KeyboardInterrupt:
            return


def run_agent_menu():
    """Run the AI Agents submenu loop."""
    import click
    
    while True:
        print_agent_menu()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if choice.lower() in ['exit', '/exit', '/quit', 'q']:
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                create_agent()
            
            elif choice == '2':
                create_crew()
            
            elif choice == '3':
                list_agents()
            
            elif choice == '4':
                list_crews()
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return
        except click.Abort:
            return


if __name__ == '__main__':
    run_agent_menu()
