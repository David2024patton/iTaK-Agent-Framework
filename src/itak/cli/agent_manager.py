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
    """Print the AI Agents submenu."""
    clear_screen()
    ensure_dirs()
    
    # Count existing agents and crews
    agents = list(AGENTS_DIR.glob('*.yaml'))
    crews = list(CREWS_DIR.glob('*.yaml'))
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🤖 AI Agents & Crews                                        ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Build and manage your AI workforce                       │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    🤖 Agents → Specialized AI with custom roles/tools        │\033[0m")
    print(f"  \033[90m│    👥 Crews  → Teams of agents working together              │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    print(f"  {BOLD}Agents:{RESET} {len(agents)} saved  |  {BOLD}Crews:{RESET} {len(crews)} saved")
    print()
    
    print(f"  {GREEN}[1]{RESET} 🤖 {WHITE}Create Agent{RESET}      {DIM}Define a new specialized agent{RESET}")
    print(f"  {GREEN}[2]{RESET} 👥 {WHITE}Create Crew{RESET}       {DIM}Build a team of agents{RESET}")
    print()
    print(f"  {GREEN}[3]{RESET} 📋 {WHITE}List Agents{RESET}       {DIM}View and manage agents{RESET}")
    print(f"  {GREEN}[4]{RESET} 📋 {WHITE}List Crews{RESET}        {DIM}View and manage crews{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()


def create_agent():
    """Wizard to create a new agent."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}🤖 Create New Agent{RESET}")
    print(f"  {DIM}Define your specialized AI agent{RESET}\n")
    
    try:
        # Agent name
        name = click.prompt(click.style("  Agent name", fg="cyan"), default="").strip()
        if not name:
            print(f"  {YELLOW}Cancelled{RESET}")
            return
        
        # Sanitize name for filename
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        
        # Role
        print(f"\n  {DIM}What is this agent's role? (e.g., 'Senior Python Developer'){RESET}")
        role = click.prompt(click.style("  Role", fg="cyan"), default="AI Assistant").strip()
        
        # Goal
        print(f"\n  {DIM}What is this agent's main goal?{RESET}")
        goal = click.prompt(click.style("  Goal", fg="cyan"), default="Help users accomplish tasks").strip()
        
        # Backstory
        print(f"\n  {DIM}Give this agent a backstory (personality, expertise){RESET}")
        backstory = click.prompt(
            click.style("  Backstory", fg="cyan"), 
            default="An experienced professional with deep expertise"
        ).strip()
        
        # Tools
        print(f"\n  {BOLD}Available Tools:{RESET}")
        available_tools = [
            ('file_read', 'Read files from disk'),
            ('file_write', 'Write/create files'),
            ('code_search', 'Search code with ripgrep'),
            ('web_search', 'Search the web'),
            ('shell', 'Execute shell commands'),
        ]
        
        for i, (tool, desc) in enumerate(available_tools, 1):
            print(f"    [{i}] {tool}: {DIM}{desc}{RESET}")
        
        print(f"\n  {DIM}Enter tool numbers separated by commas (e.g., 1,2,3){RESET}")
        tool_input = click.prompt(click.style("  Tools", fg="cyan"), default="1,2,3").strip()
        
        selected_tools = []
        try:
            for num in tool_input.split(','):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_tools):
                    selected_tools.append(available_tools[idx][0])
        except:
            selected_tools = ['file_read', 'file_write', 'code_search']
        
        # LLM
        print(f"\n  {DIM}Which LLM should this agent use?{RESET}")
        llm = click.prompt(click.style("  LLM", fg="cyan"), default="ollama/qwen3:4b").strip()
        
        # Build agent definition
        agent_def = {
            'name': name,
            'role': role,
            'goal': goal,
            'backstory': backstory,
            'tools': selected_tools,
            'llm': llm,
            'verbose': True,
            'allow_delegation': False,
        }
        
        # Save to file
        ensure_dirs()
        agent_file = AGENTS_DIR / f"{safe_name}.yaml"
        
        with open(agent_file, 'w') as f:
            yaml.dump(agent_def, f, default_flow_style=False)
        
        print(f"\n  {GREEN}✅ Agent '{name}' created!{RESET}")
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
