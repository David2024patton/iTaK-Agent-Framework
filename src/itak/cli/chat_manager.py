"""
iTaK Chat Manager
Handles chat submenu with Natural, Agent, and Crew modes
"""
import os
import sys
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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_chat_menu():
    """Print the chat submenu."""
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  💬 Chat & Conversation                                      ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Choose your conversation mode                             │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    💬 Natural → Quick Q&A with LLM (fast, simple)             │\033[0m")
    print(f"  \033[90m│    🧙 Wizard  → AI with powers (code, search, files)          │\033[0m")
    print(f"  \033[90m│    🏰 Guild   → Run a team of specialized wizards             │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    print(f"  {GREEN}[1]{RESET} 💬 {WHITE}Natural Chat{RESET}      {DIM}Quick conversation with Ollama{RESET}")
    print(f"  {GREEN}[2]{RESET} 🧙 {WHITE}Wizard Chat{RESET}       {DIM}AI with powers and capabilities{RESET}")
    print(f"  {GREEN}[3]{RESET} 🏰 {WHITE}Guild Chat{RESET}        {DIM}Run a team of wizards{RESET}")
    print()
    print(f"  {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()


def natural_chat():
    """Run simple chat with Ollama."""
    import click
    import time
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}💬 Natural Chat{RESET}")
    print(f"  {DIM}Quick Q&A with Ollama - type /back to return{RESET}\n")
    
    # Fast models recommendation
    FAST_MODELS = ['qwen3:1.7b', 'qwen3:4b', 'gemma3:4b', 'llama3.2:3b', 'phi4-mini:3.8b']
    
    try:
        import ollama
        
        # Check available models
        print(f"  {DIM}Checking Ollama models...{RESET}", end="", flush=True)
        try:
            models_response = ollama.list()
            available = [m['name'] for m in models_response.get('models', [])]
            print(f" {GREEN}✓{RESET}")
        except:
            available = []
            print(f" {YELLOW}?{RESET}")
        
        # Get model from env or pick a fast one
        model = os.environ.get('OLLAMA_MODEL', '')
        
        if not model:
            # Try to pick a fast model that's available
            for fast in FAST_MODELS:
                if any(fast.split(':')[0] in m for m in available):
                    model = fast
                    break
            if not model:
                model = 'qwen3:4b'  # Default
        
        print(f"\n  {BOLD}Model:{RESET} {CYAN}{model}{RESET}")
        
        # Show tips
        print(f"\n  {DIM}💡 Tips:{RESET}")
        print(f"  {DIM}   • First response may take 10-30s to load the model{RESET}")
        print(f"  {DIM}   • Type /model to switch models{RESET}")
        print(f"  {DIM}   • For faster responses, try: qwen3:1.7b or gemma3:4b{RESET}")
        print()
        
        history = []
        
        while True:
            try:
                user_input = click.prompt(click.style("  You", fg="cyan"), default="").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['/back', '/menu', '/exit', '/quit', '0']:
                    return
                
                # Model switch command
                if user_input.lower().startswith('/model'):
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        model = parts[1].strip()
                        print(f"\n  {GREEN}✓ Switched to: {model}{RESET}\n")
                        history = []  # Clear history for new model
                    else:
                        print(f"\n  {BOLD}Available models:{RESET}")
                        if available:
                            for m in available[:10]:
                                print(f"    • {m}")
                        else:
                            print(f"    {DIM}Run 'ollama list' to see models{RESET}")
                        print(f"\n  {DIM}Usage: /model qwen3:4b{RESET}\n")
                    continue
                
                # Add to history
                history.append({'role': 'user', 'content': user_input})
                
                # Show thinking indicator
                print(f"\n  {MAGENTA}✦{RESET} {DIM}Thinking...{RESET}", end="", flush=True)
                start_time = time.time()
                
                response_text = ""
                first_chunk = True
                
                try:
                    stream = ollama.chat(
                        model=model,
                        messages=history,
                        stream=True
                    )
                    
                    for chunk in stream:
                        if first_chunk:
                            # Clear the "Thinking..." text
                            print(f"\r  {MAGENTA}✦{RESET} ", end="", flush=True)
                            first_chunk = False
                        
                        content = chunk['message']['content']
                        print(content, end="", flush=True)
                        response_text += content
                    
                    elapsed = time.time() - start_time
                    print(f"\n  {DIM}({elapsed:.1f}s){RESET}\n")
                    
                    # Warn if slow
                    if elapsed > 30:
                        print(f"  {YELLOW}💡 Slow response. Try: /model qwen3:1.7b for faster chat{RESET}\n")
                    
                except Exception as e:
                    print(f"\r  {RED}✗ Error: {e}{RESET}\n")
                    print(f"  {DIM}Make sure Ollama is running and model exists{RESET}")
                    print(f"  {DIM}Try: ollama pull {model}{RESET}\n")
                    history.pop()  # Remove failed message from history
                    continue
                
                # Add response to history
                history.append({'role': 'assistant', 'content': response_text})
                
            except KeyboardInterrupt:
                print(f"\n\n  {DIM}Returning to menu...{RESET}")
                return
                
    except ImportError:
        print(f"\n  {YELLOW}⚠️  Ollama not installed. Run: pip install ollama{RESET}")
        input("\n  Press Enter to continue...")
    except Exception as e:
        print(f"\n  {YELLOW}⚠️  Error: {e}{RESET}")
        print(f"  {DIM}Make sure Ollama is running: ollama serve{RESET}")
        input("\n  Press Enter to continue...")


def agent_chat():
    """Run chat with a CrewAI agent."""
    import click
    import subprocess
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}🤖 Agent Chat{RESET}")
    print(f"  {DIM}AI with tools - type /back to return{RESET}\n")
    
    # Check for saved agents
    agents_dir = Path.home() / '.itak' / 'agents'
    agents = list(agents_dir.glob('*.yaml')) if agents_dir.exists() else []
    
    if agents:
        print(f"  {BOLD}Available Agents:{RESET}")
        for i, agent_file in enumerate(agents, 1):
            print(f"    [{i}] {agent_file.stem}")
        print(f"    [0] Default Agent")
        print()
        
        choice = click.prompt(click.style("  Select agent", fg="cyan"), default="0").strip()
    else:
        choice = "0"
    
    print(f"\n  {DIM}Starting agent... (this may take a moment){RESET}\n")
    
    while True:
        try:
            user_input = click.prompt(click.style("  You", fg="cyan"), default="").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/back', '/menu', '/exit', '/quit', '0']:
                return
            
            # Run itak auto command
            print(f"\n  {MAGENTA}✦{RESET} {DIM}Agent is thinking...{RESET}\n")
            
            result = subprocess.run(
                [sys.executable, "-m", "itak.cli.cli", "auto", user_input],
                capture_output=False
            )
            
            print()
            
        except KeyboardInterrupt:
            print(f"\n\n  {DIM}Returning to menu...{RESET}")
            return


def crew_chat():
    """Run a crew of agents."""
    import click
    
    clear_screen()
    print(f"\n  {BOLD}{MAGENTA}👥 Crew Chat{RESET}")
    print(f"  {DIM}Run a team of agents - type /back to return{RESET}\n")
    
    # Check for saved crews
    crews_dir = Path.home() / '.itak' / 'crews'
    crews = list(crews_dir.glob('*.yaml')) if crews_dir.exists() else []
    
    if not crews:
        print(f"  {YELLOW}⚠️  No crews defined yet.{RESET}")
        print(f"  {DIM}Go to AI Agents → Create Crew to build one.{RESET}")
        input("\n  Press Enter to continue...")
        return
    
    print(f"  {BOLD}Available Crews:{RESET}")
    for i, crew_file in enumerate(crews, 1):
        print(f"    [{i}] {crew_file.stem}")
    print()
    
    choice = click.prompt(click.style("  Select crew", fg="cyan"), default="1").strip()
    
    try:
        crew_idx = int(choice) - 1
        if 0 <= crew_idx < len(crews):
            crew_file = crews[crew_idx]
            print(f"\n  {CYAN}Running crew: {crew_file.stem}{RESET}")
            print(f"  {DIM}(Crew execution would happen here){RESET}")
        else:
            print(f"  {YELLOW}Invalid choice{RESET}")
    except ValueError:
        print(f"  {YELLOW}Invalid choice{RESET}")
    
    input("\n  Press Enter to continue...")


def run_chat_menu():
    """Run the chat submenu loop."""
    import click
    
    while True:
        print_chat_menu()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if choice.lower() in ['exit', '/exit', '/quit', 'q']:
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                natural_chat()
            
            elif choice == '2':
                agent_chat()
            
            elif choice == '3':
                crew_chat()
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return
        except click.Abort:
            return


if __name__ == '__main__':
    run_chat_menu()
