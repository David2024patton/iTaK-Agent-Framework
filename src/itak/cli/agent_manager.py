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


def create_agent():
    """Wizard to create a new wizard (agent)."""
    import click
    import sys
    
    clear_screen()
    
    # Themed header
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🧙 Create New Wizard                                        ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Define a specialized AI wizard with unique powers         │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│     Type /exit at any time to cancel                          │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    try:
        # Step 1: Name
        print(f"  {BOLD}Step 1 of 5: Wizard Name{RESET}")
        print(f"  {DIM}Give your wizard a memorable name{RESET}")
        name = click.prompt(click.style("  Name", fg="cyan"), default="", show_default=False).strip()
        
        if not name or name.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            input("\n  Press Enter to continue...")
            return
        
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        print(f"  {GREEN}✓{RESET} {name}\n")
        
        # Step 2: Role
        print(f"  {BOLD}Step 2 of 5: Role{RESET}")
        print(f"  {DIM}What is this wizard's specialty? (e.g., 'Senior Python Developer'){RESET}")
        role = click.prompt(click.style("  Role", fg="cyan"), default="AI Assistant", show_default=False).strip()
        if role.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            return
        print(f"  {GREEN}✓{RESET} {role}\n")
        
        # Step 3: Goal
        print(f"  {BOLD}Step 3 of 5: Mission{RESET}")
        print(f"  {DIM}What is this wizard's primary mission?{RESET}")
        goal = click.prompt(click.style("  Mission", fg="cyan"), default="Help users accomplish tasks", show_default=False).strip()
        if goal.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            return
        print(f"  {GREEN}✓{RESET} {goal}\n")
        
        # Step 4: Powers (Tools)
        print(f"  {BOLD}Step 4 of 5: Powers{RESET}")
        print(f"  {DIM}Select the magical powers for this wizard{RESET}\n")
        
        available_tools = [
            ('📖 file_read', 'file_read', 'Read files from disk'),
            ('✍️ file_write', 'file_write', 'Write/create files'),
            ('🔍 code_search', 'code_search', 'Search code with ripgrep'),
            ('🌐 web_search', 'web_search', 'Search the web'),
            ('⚡ shell', 'shell', 'Execute shell commands'),
        ]
        
        for i, (display, tool, desc) in enumerate(available_tools, 1):
            print(f"    [{CYAN}{i}{RESET}] {display}  {DIM}{desc}{RESET}")
        
        print(f"\n  {DIM}Enter numbers separated by commas (e.g., 1,2,3){RESET}")
        tool_input = click.prompt(click.style("  Powers", fg="cyan"), default="1,2,3", show_default=False).strip()
        
        if tool_input.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            return
        
        selected_tools = []
        try:
            for num in tool_input.split(','):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_tools):
                    selected_tools.append(available_tools[idx][1])
        except:
            selected_tools = ['file_read', 'file_write', 'code_search']
        
        print(f"  {GREEN}✓{RESET} {len(selected_tools)} powers selected\n")
        
        # Step 5: LLM
        print(f"  {BOLD}Step 5 of 5: Brain{RESET}")
        print(f"  {DIM}Which model will power this wizard?{RESET}")
        llm = click.prompt(click.style("  Model", fg="cyan"), default="ollama/qwen3:4b", show_default=False).strip()
        if llm.lower() in ['/exit', 'exit']:
            print(f"\n  {YELLOW}Cancelled{RESET}")
            return
        print(f"  {GREEN}✓{RESET} {llm}\n")
        
        # Build and save
        agent_def = {
            'name': name,
            'role': role,
            'goal': goal,
            'backstory': f"A skilled {role} wizard with expertise in their craft",
            'tools': selected_tools,
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
        print(f"  {BOLD}Powers:{RESET}  {', '.join(selected_tools)}")
        print(f"  {BOLD}Brain:{RESET}   {llm}")
        print()
        print(f"  {DIM}Saved to: {agent_file}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Cancelled{RESET}")
    except click.Abort:
        pass
    
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
