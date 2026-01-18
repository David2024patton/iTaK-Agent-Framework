"""
iTaK CLI REPL - Gemini-Style Interactive Chat

Read-Eval-Print Loop for continuous conversation with the AI.
"""

import os
import sys
from pathlib import Path
from typing import Optional

from .banner import (
    print_banner,
    print_welcome_tips,
    print_prompt,
    print_response_start,
    print_awaiting,
    print_model_info,
    print_status_bar,
    print_code_block,
    print_file_operation,
    RESET, DIM, CYAN, GREEN, YELLOW, WHITE, MAGENTA, BOLD
)


class iTaKREPL:
    """Interactive REPL for iTaK CLI."""
    
    def __init__(self, model: str = "qwen3-vl:2b"):
        self.model = model
        self.running = True
        self.context_files = []
        self.history = []
        
    def start(self):
        """Start the REPL."""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print banner
        print_banner("large")
        
        # Get terminal width for formatting
        import shutil
        term_width = shutil.get_terminal_size().columns
        
        # Startup Menu - "What type of project would you like to build?"
        print(f"\n  {BOLD}What type of project would you like to build?{RESET}\n")
        
        from .wizard import PROJECT_TYPES
        
        # Calculate max description length to avoid wrap
        prefix_len = 8  # "    [N] " 
        # Shorten descriptions if terminal is narrow
        short_descs = {
            "HTML/CSS/JavaScript web application": "Web app",
            "Python script or automation": "Python script",
            "REST API or backend service": "API service",
            "AI agent or automation workflow": "AI workflow",
            "Describe your project freely": "Custom project",
        }
        
        # Print Wizard Options [1-5]
        for i, (name, _, desc) in enumerate(PROJECT_TYPES, 1):
            # Use short desc if terminal is narrow
            display_desc = short_descs.get(desc, desc) if term_width < 80 else desc
            print(f"    {GREEN}[{i}]{RESET} {name} {DIM}- {display_desc}{RESET}")
            
        # Print Chat Option [6]
        chat_desc = "Chat/test models" if term_width < 80 else "Interactive general coding assistance"
        print(f"    {GREEN}[6]{RESET} {MAGENTA}💬 Chat with AI{RESET} {DIM}- {chat_desc}{RESET}")
        print()
        
        # Get choice - smart input: numbers select menu, text goes to chat
        import click
        initial_message = None
        
        while True:
            try:
                raw_input = click.prompt(click.style("  Choice", fg="cyan"), default="6")
                stripped = raw_input.strip().lower()
                
                # Handle exit commands at menu level
                if stripped in ['/exit', '/quit', '/q', 'exit', 'quit', 'q']:
                    print(f"\n{YELLOW}Goodbye!{RESET}\n")
                    return
                
                # Try to parse as number
                try:
                    choice = int(raw_input.strip())
                    if 1 <= choice <= 6:
                        break
                    print(f"  {YELLOW}Please enter 1-6, or just type your question{RESET}")
                except ValueError:
                    # Not a number - treat as chat message and auto-select option 6
                    choice = 6
                    initial_message = raw_input.strip()
                    break
                    
            except click.Abort:
                return
        
        # Handle Choice
        if choice == 6:
            # Clear screen for fresh Chat mode view
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n  {BOLD}{MAGENTA}💬 Chat Mode{RESET}")
            print(f"  {DIM}Type your questions, or /menu to go back{RESET}\n")
            
            print_welcome_tips()
            
            # If user typed a message at the menu, process it immediately
            if initial_message:
                # Show the prompt so user knows what was sent
                print(f"{CYAN}>{RESET} {initial_message}")
                print()
                self.history.append(initial_message)
                self.process_prompt(initial_message)
            
            # Main loop
            while self.running:
                try:
                    self.run_once()
                except KeyboardInterrupt:
                    print(f"\n\n{DIM}Use /exit to quit or Ctrl+C again to force exit.{RESET}")
                    try:
                        self.run_once()
                    except KeyboardInterrupt:
                        self.running = False
                        print(f"\n{YELLOW}Goodbye!{RESET}\n")
                except EOFError:
                    self.running = False
                    print(f"\n{YELLOW}Goodbye!{RESET}\n")
        
        else:
            # Wizard Mode [1-5] - Clear screen for fresh view
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                from .wizard import run_project_wizard
                run_project_wizard(project_type_idx=choice)
            except ImportError:
                print(f"\n{YELLOW}Wizard module not available.{RESET}\n")
            except Exception as e:
                print(f"\n{YELLOW}Error running wizard: {e}{RESET}\n")
    
    def run_once(self):
        """Run one iteration of the REPL."""
        print_prompt()
        
        try:
            user_input = input().strip()
        except:
            return
        
        if not user_input:
            return
        
        # Handle slash commands
        if user_input.startswith('/'):
            self.handle_command(user_input)
            return
        
        # Handle @file references
        if '@' in user_input:
            user_input = self.resolve_file_references(user_input)
        
        # Add to history
        self.history.append(user_input)
        
        # Process the prompt
        self.process_prompt(user_input)
    
    def handle_command(self, command: str):
        """Handle slash commands."""
        cmd = command.lower().split()[0]
        args = command.split()[1:] if len(command.split()) > 1 else []
        
        if cmd in ['/exit', '/quit', '/q']:
            self.running = False
            print(f"\n{YELLOW}Goodbye!{RESET}\n")
            
        elif cmd in ['/help', '/h', '/?']:
            self.show_help()
            
        elif cmd in ['/clear', '/cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner("large")
            
        elif cmd == '/model':
            if args:
                self.model = args[0]
                print(f"\n{GREEN}✓{RESET} Model set to: {CYAN}{self.model}{RESET}\n")
            else:
                print(f"\n  Current model: {CYAN}{self.model}{RESET}")
                print(f"  Usage: /model <model_name>\n")
                
        elif cmd == '/studio':
            self.launch_studio()
            
        elif cmd == '/models':
            self.show_models()
            
        elif cmd == '/status':
            self.show_status()
        
        elif cmd in ['/create', '/new']:
            self.create_project()
        
        elif cmd == '/ide':
            self.handle_ide_command(args)
        
        elif cmd == '/menu':
            # Return to main menu
            self.running = False
            print(f"\n{CYAN}Returning to main menu...{RESET}\n")
            self.start()  # Restart the startup menu
            
        else:
            print(f"\n{YELLOW}Unknown command: {cmd}{RESET}")
            print(f"{DIM}Type /help for available commands.{RESET}\n")
    
    def show_help(self):
        """Show help for slash commands."""
        print(f"""
{BOLD}Available Commands:{RESET}

  {GREEN}/help{RESET}       Show this help message
  {GREEN}/menu{RESET}       Return to main menu
  {GREEN}/clear{RESET}      Clear the screen
  {GREEN}/model{RESET}      Show or change the current model
  {GREEN}/models{RESET}     Browse available models
  {GREEN}/create{RESET}     Create a new project
  {GREEN}/studio{RESET}     Launch the web-based Studio UI
  {GREEN}/status{RESET}     Show current status
  {GREEN}/ide{RESET}        IDE integration (install, enable, status)
  {GREEN}/exit{RESET}       Exit the CLI

{BOLD}IDE Commands:{RESET}
  {CYAN}/ide status{RESET}   Check IDE connection status
  {CYAN}/ide install{RESET}  Install the VS Code companion extension
  {CYAN}/ide enable{RESET}   Enable IDE integration
  {CYAN}/ide disable{RESET}  Disable IDE integration

{BOLD}Tips:{RESET}
  - Use {CYAN}@path/to/file{RESET} to reference files
  - Be specific for the best results
  - Press Ctrl+C to cancel current operation
""")
    
    def show_status(self):
        """Show current status."""
        print(f"""
{BOLD}Status:{RESET}
  Model: {CYAN}{self.model}{RESET}
  Context files: {len(self.context_files)}
  History: {len(self.history)} messages
  Working dir: {os.getcwd()}
""")
    
    def show_models(self):
        """Browse and select models from categories."""
        try:
            from .model_browser import browse_models
            selected = browse_models(self.model)
            if selected != self.model:
                self.model = selected
                print(f"  {DIM}Model changed to {CYAN}{self.model}{RESET}")
        except ImportError:
            print(f"\n{YELLOW}Model browser not available.{RESET}\n")
    
    def launch_studio(self):
        """Launch the Studio web UI."""
        print(f"\n{CYAN}🌐 Launching Studio...{RESET}\n")
        try:
            from .studio_launcher import launch_studio
            launch_studio()
        except ImportError:
            print(f"{YELLOW}Studio not available.{RESET}\n")
    
    def resolve_file_references(self, text: str) -> str:
        """Resolve @file references to actual file contents."""
        import re
        
        pattern = r'@(\S+)'
        matches = re.findall(pattern, text)
        
        for match in matches:
            filepath = Path(match)
            if filepath.exists() and filepath.is_file():
                try:
                    content = filepath.read_text(errors='ignore')[:5000]  # Limit size
                    self.context_files.append(str(filepath))
                    text = text.replace(f'@{match}', f'\n[File: {match}]\n```\n{content}\n```\n')
                    print(f"  {GREEN}✓{RESET} Loaded: {match}")
                except Exception as e:
                    print(f"  {YELLOW}⚠{RESET} Could not read: {match}")
        
        return text
    
    def create_project(self):
        """Launch the project creation wizard."""
        print(f"\n{CYAN}📁 Creating new project...{RESET}\n")
        try:
            from .wizard import run_project_wizard
            run_project_wizard()
        except ImportError:
            print(f"{YELLOW}Project wizard not available.{RESET}\n")
        except Exception as e:
            print(f"{YELLOW}Error: {e}{RESET}\n")
    
    def handle_ide_command(self, args: list):
        """Handle IDE integration commands."""
        if not args:
            self.show_ide_status()
            return
        
        subcmd = args[0].lower()
        
        if subcmd == 'status':
            self.show_ide_status()
        elif subcmd == 'install':
            self.install_ide_extension()
        elif subcmd == 'enable':
            self.enable_ide()
        elif subcmd == 'disable':
            self.disable_ide()
        else:
            print(f"\n{YELLOW}Unknown /ide command: {subcmd}{RESET}")
            print(f"Options: status, install, enable, disable\n")
    
    def show_ide_status(self):
        """Show IDE integration status."""
        import os
        
        # Check for IDE environment variables (set by VS Code companion)
        ide_port = os.environ.get('ITAK_CLI_IDE_SERVER_PORT')
        ide_workspace = os.environ.get('ITAK_CLI_IDE_WORKSPACE_PATH')
        
        print(f"\n{BOLD}IDE Integration Status:{RESET}")
        
        if ide_port:
            print(f"  {GREEN}🟢{RESET} Connected to IDE")
            print(f"  Port: {ide_port}")
            if ide_workspace:
                print(f"  Workspace: {ide_workspace}")
        else:
            print(f"  {YELLOW}🔴{RESET} Not connected to IDE")
            print(f"\n  {DIM}To enable IDE integration:{RESET}")
            print(f"  1. Install the iTaK CLI Companion extension in VS Code")
            print(f"  2. Run iTaK from VS Code's integrated terminal")
        print()
    
    def install_ide_extension(self):
        """Install the IDE companion extension."""
        print(f"\n{CYAN}📦 Installing iTaK CLI Companion extension...{RESET}\n")
        
        # Check if VS Code is available
        import subprocess
        try:
            result = subprocess.run(
                ["code", "--install-extension", "itak.itak-cli-companion"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  {GREEN}✓{RESET} Extension installed successfully!")
                print(f"  Restart VS Code to activate.\n")
            else:
                print(f"  {YELLOW}⚠{RESET} Extension not yet available on marketplace.")
                print(f"  {DIM}Coming soon!{RESET}\n")
        except FileNotFoundError:
            print(f"  {YELLOW}⚠{RESET} VS Code CLI not found.")
            print(f"  Make sure VS Code is installed and 'code' is in your PATH.\n")
    
    def enable_ide(self):
        """Enable IDE integration."""
        print(f"\n{GREEN}✓{RESET} IDE integration enabled.")
        print(f"  {DIM}Run iTaK from VS Code's terminal for full integration.{RESET}\n")
    
    def disable_ide(self):
        """Disable IDE integration."""
        print(f"\n{YELLOW}✓{RESET} IDE integration disabled.\n")
    
    def process_prompt(self, prompt: str):
        """Process a user prompt and generate response."""
        print_model_info(self.model)
        
        # Try to run the auto command
        try:
            self.run_auto_command(prompt)
        except Exception as e:
            print(f"\n{MAGENTA}✦{RESET} I'll help you with that.\n")
            print(f"  {DIM}(AI response would appear here){RESET}")
            print(f"  {DIM}Error: {e}{RESET}")
        
        print_awaiting()
    
    def run_auto_command(self, prompt: str):
        """Run the iTaK auto command with the prompt."""
        import subprocess
        
        # Run itak auto as subprocess
        result = subprocess.run(
            [sys.executable, "-m", "itak.cli.cli", "auto", prompt],
            capture_output=False
        )


def run_repl(model: str = "qwen3-vl:2b"):
    """Start the iTaK REPL."""
    repl = iTaKREPL(model=model)
    repl.start()


if __name__ == "__main__":
    run_repl()
