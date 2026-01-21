"""
iTaK Powers (Skills) Manager
Handles skill creation and management for agents
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

# Config directory
SKILLS_DIR = Path.home() / '.itak' / 'skills'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def ensure_dirs():
    """Ensure config directories exist."""
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def print_powers_menu():
    """Print the Powers (Skills) submenu."""
    clear_screen()
    ensure_dirs()
    
    # Count existing skills
    skills = list(SKILLS_DIR.glob('*.yaml'))
    
    # Also check project skills
    project_skills = Path('.agent/skills')
    local_skills = list(project_skills.glob('*/SKILL.md')) if project_skills.exists() else []
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  ⚡ Powers & Skills                                          ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Skills are reusable capabilities for your agents          │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    🔧 Tools   → Code execution, file ops, web search          │\033[0m")
    print(f"  \033[90m│    📚 Skills  → Multi-step workflows with instructions        │\033[0m")
    print(f"  \033[90m│    🔌 MCP     → Model Context Protocol integrations           │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    print(f"  {BOLD}Custom Skills:{RESET} {len(skills)} saved  |  {BOLD}Project Skills:{RESET} {len(local_skills)}")
    print()
    
    print(f"  {GREEN}[1]{RESET} ⚡ {WHITE}List Built-in Tools{RESET}  {DIM}View available agent tools{RESET}")
    print(f"  {GREEN}[2]{RESET} 📚 {WHITE}List Skills{RESET}          {DIM}View custom skills{RESET}")
    print(f"  {GREEN}[3]{RESET} ✨ {WHITE}Create Skill{RESET}         {DIM}Define a new skill{RESET}")
    print()
    print(f"  {GREEN}[4]{RESET} 🔌 {WHITE}MCP Servers{RESET}          {DIM}Manage MCP integrations{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()


def list_builtin_tools():
    """List all built-in agent tools."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}⚡ Built-in Agent Tools{RESET}\n")
    
    tools = [
        ("file_read", "Read contents of files from disk", "📄"),
        ("file_write", "Create or modify files", "✏️"),
        ("file_delete", "Delete files from disk", "🗑️"),
        ("directory_list", "List contents of directories", "📁"),
        ("code_search", "Search code with ripgrep (fast)", "🔍"),
        ("web_search", "Search the web via SearXNG", "🌐"),
        ("web_scrape", "Extract content from web pages", "🕷️"),
        ("shell_execute", "Run shell commands", "💻"),
        ("python_execute", "Execute Python code", "🐍"),
        ("git_operations", "Git add, commit, push, etc", "📦"),
        ("docker_manage", "Docker container operations", "🐳"),
        ("ollama_chat", "Chat with local LLMs", "🤖"),
        ("browser_action", "Automate web browsers", "🌐"),
    ]
    
    for name, desc, icon in tools:
        print(f"  {icon} {CYAN}{name}{RESET}")
        print(f"     {DIM}{desc}{RESET}")
    
    print(f"\n  {DIM}These tools can be assigned to agents when creating them.{RESET}")
    input("\n  Press Enter to continue...")


def list_skills():
    """List custom skills."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}📚 Custom Skills{RESET}\n")
    
    skills = list(SKILLS_DIR.glob('*.yaml'))
    
    # Also check project skills
    project_skills = Path('.agent/skills')
    local_skills = []
    if project_skills.exists():
        for skill_dir in project_skills.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / 'SKILL.md'
                if skill_file.exists():
                    local_skills.append(skill_dir)
    
    if not skills and not local_skills:
        print(f"  {DIM}No custom skills defined yet.{RESET}")
        print(f"  {DIM}Use 'Create Skill' to build one.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    if local_skills:
        print(f"  {BOLD}Project Skills (.agent/skills/):{RESET}")
        for skill_dir in local_skills:
            print(f"    📚 {CYAN}{skill_dir.name}{RESET}")
        print()
    
    if skills:
        print(f"  {BOLD}Global Skills (~/.itak/skills/):{RESET}")
        for i, skill_file in enumerate(skills, 1):
            try:
                with open(skill_file) as f:
                    skill = yaml.safe_load(f)
                print(f"    [{i}] {CYAN}{skill.get('name', skill_file.stem)}{RESET}")
                print(f"        {DIM}{skill.get('description', 'No description')}{RESET}")
            except:
                print(f"    [{i}] {skill_file.stem} {YELLOW}(error reading){RESET}")
    
    input("\n  Press Enter to continue...")


def create_skill():
    """Wizard to create a new skill."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}✨ Create New Skill{RESET}")
    print(f"  {DIM}Skills are reusable workflows for your agents{RESET}\n")
    
    try:
        # Skill name
        name = click.prompt(click.style("  Skill name", fg="cyan"), default="").strip()
        if not name:
            print(f"  {YELLOW}Cancelled{RESET}")
            return
        
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        
        # Description
        print(f"\n  {DIM}Describe what this skill does{RESET}")
        description = click.prompt(
            click.style("  Description", fg="cyan"), 
            default="A custom skill"
        ).strip()
        
        # Instructions
        print(f"\n  {DIM}Provide step-by-step instructions for the agent{RESET}")
        print(f"  {DIM}(Enter multiple lines, empty line to finish){RESET}")
        
        instructions = []
        step = 1
        while True:
            line = click.prompt(
                click.style(f"  Step {step}", fg="cyan"), 
                default=""
            ).strip()
            if not line:
                break
            instructions.append(f"{step}. {line}")
            step += 1
        
        if not instructions:
            instructions = ["1. Follow the user's request carefully"]
        
        # Tools needed
        print(f"\n  {BOLD}Tools this skill needs:{RESET}")
        available_tools = ['file_read', 'file_write', 'code_search', 'web_search', 'shell_execute', 'python_execute']
        for i, tool in enumerate(available_tools, 1):
            print(f"    [{i}] {tool}")
        
        print(f"\n  {DIM}Enter tool numbers separated by commas (or leave empty){RESET}")
        tool_input = click.prompt(click.style("  Tools", fg="cyan"), default="").strip()
        
        selected_tools = []
        if tool_input:
            try:
                for num in tool_input.split(','):
                    idx = int(num.strip()) - 1
                    if 0 <= idx < len(available_tools):
                        selected_tools.append(available_tools[idx])
            except:
                pass
        
        # Build skill definition
        skill_def = {
            'name': name,
            'description': description,
            'instructions': '\n'.join(instructions),
            'tools': selected_tools,
            'version': '1.0',
        }
        
        # Save to file
        ensure_dirs()
        skill_file = SKILLS_DIR / f"{safe_name}.yaml"
        
        with open(skill_file, 'w') as f:
            yaml.dump(skill_def, f, default_flow_style=False)
        
        print(f"\n  {GREEN}✅ Skill '{name}' created!{RESET}")
        print(f"  {DIM}Saved to: {skill_file}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Cancelled{RESET}")
    except click.Abort:
        pass
    
    input("\n  Press Enter to continue...")


def manage_mcp():
    """Manage MCP server integrations."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}🔌 MCP Server Integrations{RESET}")
    print(f"  {DIM}Model Context Protocol servers extend agent capabilities{RESET}\n")
    
    # Check for mcp config
    mcp_config = Path.home() / '.itak' / 'mcp_servers.yaml'
    
    if mcp_config.exists():
        try:
            with open(mcp_config) as f:
                servers = yaml.safe_load(f) or {}
            
            if servers:
                print(f"  {BOLD}Configured MCP Servers:{RESET}\n")
                for name, config in servers.items():
                    status = f"{GREEN}●{RESET}" if config.get('enabled', True) else f"{RED}○{RESET}"
                    print(f"    {status} {CYAN}{name}{RESET}")
                    print(f"       {DIM}{config.get('description', 'No description')}{RESET}")
            else:
                print(f"  {DIM}No MCP servers configured.{RESET}")
        except:
            print(f"  {YELLOW}Error reading MCP config{RESET}")
    else:
        print(f"  {DIM}No MCP servers configured yet.{RESET}")
    
    print(f"\n  {DIM}MCP servers can be configured in:{RESET}")
    print(f"  {DIM}{mcp_config}{RESET}")
    
    input("\n  Press Enter to continue...")


def run_powers_menu():
    """Run the Powers submenu loop."""
    import click
    
    while True:
        print_powers_menu()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if choice.lower() in ['exit', '/exit', '/quit', 'q']:
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                list_builtin_tools()
            
            elif choice == '2':
                list_skills()
            
            elif choice == '3':
                create_skill()
            
            elif choice == '4':
                manage_mcp()
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return
        except click.Abort:
            return


if __name__ == '__main__':
    run_powers_menu()
