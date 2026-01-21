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
        'llm': 'ollama/qwen3:4b'
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
        
        if choice.lower() in ['/exit', 'exit', '0', '']:
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

            response = ollama.chat(model='qwen3:4b', messages=[
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
            print(f"  {BOLD}Brain:{RESET}   ollama/qwen3:4b")
            print()
            
            confirm = click.prompt(click.style("  Create this wizard? [Y/n]", fg="cyan"), default="y", show_default=False).strip().lower()
            
            if confirm in ['y', 'yes', '']:
                save_wizard(name, role, goal, tools, 'ollama/qwen3:4b')
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
    """Create wizard from pre-built template."""
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
                
                # Ask for custom name
                print(f"\n  {DIM}Customize the wizard name (or press Enter for default){RESET}")
                custom_name = click.prompt(
                    click.style("  Name", fg="cyan"), 
                    default=template['name'], 
                    show_default=False
                ).strip()
                
                save_wizard(
                    custom_name,
                    template['role'],
                    template['goal'],
                    template['tools'],
                    template['llm']
                )
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
        llm = click.prompt(click.style("  Model", fg="cyan"), default="ollama/qwen3:4b", show_default=False).strip()
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




def create_crew():
    """Wizard to create a new crew."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}👥 Create New Crew{RESET}")
    print(f"  {DIM}Build a team of agents that work together{RESET}\n")
    
    # Check for existing agents
    agents = list(AGENTS_DIR.glob('*.yaml'))
    
    if not agents:
        print(f"  {YELLOW}⚠️  No agents defined yet.{RESET}")
        print(f"  {DIM}Create some agents first with 'Create Agent'.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    try:
        # Crew name
        name = click.prompt(click.style("  Crew name", fg="cyan"), default="").strip()
        if not name:
            print(f"  {YELLOW}Cancelled{RESET}")
            return
        
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        
        # Show available agents
        print(f"\n  {BOLD}Available Agents:{RESET}")
        for i, agent_file in enumerate(agents, 1):
            print(f"    [{i}] {agent_file.stem}")
        
        print(f"\n  {DIM}Select agents by number, separated by commas (e.g., 1,2,3){RESET}")
        agent_input = click.prompt(click.style("  Agents", fg="cyan"), default="").strip()
        
        selected_agents = []
        try:
            for num in agent_input.split(','):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(agents):
                    selected_agents.append(agents[idx].stem)
        except:
            pass
        
        if not selected_agents:
            print(f"  {YELLOW}No agents selected{RESET}")
            return
        
        # Workflow type
        print(f"\n  {BOLD}Workflow Types:{RESET}")
        print(f"    [1] Sequential - Agents work one after another")
        print(f"    [2] Hierarchical - Manager assigns tasks to agents")
        
        workflow = click.prompt(click.style("  Workflow", fg="cyan"), default="1").strip()
        workflow_type = "hierarchical" if workflow == "2" else "sequential"
        
        # Build crew definition
        crew_def = {
            'name': name,
            'agents': selected_agents,
            'workflow': workflow_type,
            'verbose': True,
        }
        
        # Save to file
        ensure_dirs()
        crew_file = CREWS_DIR / f"{safe_name}.yaml"
        
        with open(crew_file, 'w') as f:
            yaml.dump(crew_def, f, default_flow_style=False)
        
        print(f"\n  {GREEN}✅ Crew '{name}' created with {len(selected_agents)} agents!{RESET}")
        print(f"  {DIM}Saved to: {crew_file}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Cancelled{RESET}")
    except click.Abort:
        pass
    
    input("\n  Press Enter to continue...")


def list_agents():
    """List and manage agents."""
    import click
    
    while True:
        clear_screen()
        print(f"\n  {BOLD}{MAGENTA}📋 Saved Agents{RESET}\n")
        
        agents = list(AGENTS_DIR.glob('*.yaml'))
        
        if not agents:
            print(f"  {DIM}No agents defined yet.{RESET}")
            print(f"  {DIM}Use 'Create Agent' to build one.{RESET}")
            input("\n  Press Enter to go back...")
            return
        
        for i, agent_file in enumerate(agents, 1):
            try:
                with open(agent_file) as f:
                    agent = yaml.safe_load(f)
                print(f"  [{i}] {CYAN}{agent.get('name', agent_file.stem)}{RESET}")
                print(f"      {DIM}Role: {agent.get('role', 'N/A')}{RESET}")
                print(f"      {DIM}Tools: {', '.join(agent.get('tools', []))}{RESET}")
            except:
                print(f"  [{i}] {agent_file.stem} {YELLOW}(error reading){RESET}")
        
        print(f"\n  {DIM}Enter number to delete, or 0 to go back{RESET}")
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if choice == '0' or choice == '':
                return
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(agents):
                    agent_file = agents[idx]
                    confirm = click.prompt(
                        click.style(f"  Delete {agent_file.stem}? (y/N)", fg="yellow"),
                        default="n"
                    ).strip().lower()
                    
                    if confirm == 'y':
                        agent_file.unlink()
                        print(f"  {GREEN}✅ Deleted{RESET}")
            except ValueError:
                pass
                
        except KeyboardInterrupt:
            return


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
