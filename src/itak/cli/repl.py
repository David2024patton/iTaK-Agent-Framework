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
    
    def __init__(self, model: str = "qwen3-vl:4b"):
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
        print_welcome_tips()
        
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
            
        else:
            print(f"\n{YELLOW}Unknown command: {cmd}{RESET}")
            print(f"{DIM}Type /help for available commands.{RESET}\n")
    
    def show_help(self):
        """Show help for slash commands."""
        print(f"""
{BOLD}Available Commands:{RESET}

  {GREEN}/help{RESET}       Show this help message
  {GREEN}/clear{RESET}      Clear the screen
  {GREEN}/model{RESET}      Show or change the current model
  {GREEN}/models{RESET}     Browse available models
  {GREEN}/studio{RESET}     Launch the web-based Studio UI
  {GREEN}/status{RESET}     Show current status
  {GREEN}/exit{RESET}       Exit the CLI

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
        """Show available models."""
        try:
            from .model_selector import display_model_menu
            display_model_menu()
        except ImportError:
            print(f"\n{YELLOW}Model catalog not available.{RESET}")
            print(f"Run: {CYAN}itak models --list{RESET}\n")
    
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


def run_repl(model: str = "qwen3-vl:4b"):
    """Start the iTaK REPL."""
    repl = iTaKREPL(model=model)
    repl.start()


if __name__ == "__main__":
    run_repl()
