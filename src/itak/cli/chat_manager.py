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
RED = "\033[31m"
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
    
    # Styled header box
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  💬 Natural Chat                                             ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Quick Q&A with your local LLM                             │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    /model     → Switch to a different model                   │\033[0m")
    print(f"  \033[90m│    /save      → Export chat to markdown file                  │\033[0m")
    print(f"  \033[90m│    /menu or 0 → Return to main menu                           │\033[0m")
    print(f"  \033[90m│    /exit      → Quit iTaK CLI                                 │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    # Fast models recommendation
    FAST_MODELS = ['qwen3:1.7b', 'qwen3:4b', 'gemma3:4b', 'llama3.2:3b', 'phi4-mini:3.8b']
    
    try:
        import ollama
        
        # Check available models
        print(f"  {DIM}Checking Ollama...{RESET}", end="", flush=True)
        try:
            models_response = ollama.list()
            available = [m['name'] for m in models_response.get('models', [])]
            print(f" {GREEN}✓{RESET} ({len(available)} models)")
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
        
        print(f"  {BOLD}Model:{RESET} {CYAN}{model}{RESET}")
        print(f"  {DIM}First response may take 10-30s to load{RESET}")
        print()
        
        # System prompt with formatting guidelines and values
        system_prompt = """You are a helpful, positive AI assistant named iTaK Wizard. Follow these guidelines strictly:

## FORMATTING RULES
• NEVER use dashes (—, -, –) or horizontal lines in your responses
• NEVER use the word "fluff" or phrases like "no fluff"
• Use bullet points with • or numbered lists instead of dashes
• Keep responses concise and direct

## SAFETY GUARDRAILS (CRITICAL)
If anyone mentions self-harm, suicide, depression, or feeling hopeless:
• Immediately express genuine care and concern
• Encourage them to call 911 or a crisis helpline (988 Suicide & Crisis Lifeline)
• Suggest talking to a parent, trusted adult, pastor, or close friend
• Offer words of hope and remind them they are valued and loved
• Offer to pray for them if they would like

## CORE VALUES
• Always be positive, uplifting, and encouraging
• Embody good moral values: honesty, integrity, kindness, respect, and hard work
• Be patriotic and express love for America and its founding principles
• Support law and order, respect for authority, and personal responsibility
• When discussing politics, lean toward traditional conservative/republican values
• Support the Constitution, individual liberty, and limited government
• Do NOT preach about religion unless specifically asked, but embody Christian values naturally
• If asked about faith or prayer, be open and supportive
• Always encourage people to do the right thing

## PERSONALITY
• Be friendly, warm, and helpful
• Be encouraging and never judgmental
• Focus on solutions and positive outcomes
• Celebrate hard work, family, faith, and community"""
        
        history = [{'role': 'system', 'content': system_prompt}]
        
        while True:
            try:
                user_input = click.prompt(click.style("  You ✨", fg="cyan"), default="", show_default=False).strip()
                
                if not user_input:
                    continue
                
                # Exit CLI completely
                if user_input.lower() in ['/exit', '/quit', 'exit', 'quit']:
                    print(f"\n{YELLOW}Goodbye!{RESET}\n")
                    sys.exit(0)
                
                # Go back to menu
                if user_input.lower() in ['/back', '/menu', '0']:
                    return
                
                # Model switch command
                if user_input.lower() == '/model':
                    # Comprehensive model capability database - emoji only for type
                    MODEL_INFO = {
                        # Qwen models
                        'qwen3-vl': {'emoji': '🧠👁️', 'speed': 'Slower'},
                        'qwen-vl': {'emoji': '👁️', 'speed': 'Medium'},
                        'qwen3': {'emoji': '🧠', 'speed': 'Slower'},
                        'qwen2.5-coder': {'emoji': '💻', 'speed': 'Medium'},
                        'qwen2.5': {'emoji': '⚡', 'speed': 'Quick'},
                        'qwq': {'emoji': '🧠', 'speed': 'Slower'},
                        
                        # DeepSeek models
                        'deepseek-r1': {'emoji': '🧠', 'speed': 'Slower'},
                        'deepseek-coder': {'emoji': '💻', 'speed': 'Medium'},
                        'deepseek-v3': {'emoji': '🧠', 'speed': 'Slower'},
                        
                        # Llama models
                        'llama3.2-vision': {'emoji': '👁️', 'speed': 'Medium'},
                        'llama3.3': {'emoji': '⚡', 'speed': 'Quick'},
                        'llama3.2': {'emoji': '⚡', 'speed': 'Quick'},
                        'llama3.1': {'emoji': '⚡', 'speed': 'Quick'},
                        'codellama': {'emoji': '💻', 'speed': 'Medium'},
                        
                        # Gemma models
                        'gemma3': {'emoji': '⚡', 'speed': 'Quick'},
                        'gemma2': {'emoji': '⚡', 'speed': 'Quick'},
                        'codegemma': {'emoji': '💻', 'speed': 'Medium'},
                        
                        # Phi models
                        'phi4': {'emoji': '🧠', 'speed': 'Medium'},
                        'phi3.5': {'emoji': '⚡', 'speed': 'Quick'},
                        'phi3': {'emoji': '⚡', 'speed': 'Quick'},
                        
                        # Vision models
                        'llava': {'emoji': '👁️', 'speed': 'Medium'},
                        'bakllava': {'emoji': '👁️', 'speed': 'Medium'},
                        'moondream': {'emoji': '👁️', 'speed': 'Quick'},
                        'minicpm-v': {'emoji': '👁️', 'speed': 'Medium'},
                        
                        # Mistral models
                        'mistral': {'emoji': '⚡', 'speed': 'Quick'},
                        'mixtral': {'emoji': '🔥', 'speed': 'Slow'},
                        
                        # Other
                        'starcoder': {'emoji': '💻', 'speed': 'Medium'},
                        'wizardcoder': {'emoji': '💻', 'speed': 'Medium'},
                        'nous-hermes': {'emoji': '⚡', 'speed': 'Quick'},
                        'neural-chat': {'emoji': '💬', 'speed': 'Quick'},
                        'openchat': {'emoji': '💬', 'speed': 'Quick'},
                    }
                    
                    def get_model_info(name):
                        name_lower = name.lower()
                        for key in sorted(MODEL_INFO.keys(), key=len, reverse=True):
                            if key in name_lower:
                                return MODEL_INFO[key]
                        return {'emoji': '💬', 'speed': 'Medium'}
                    
                    # Clear and show model selector
                    clear_screen()
                    
                    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
                    print(f"  \033[35m║  🔮 Model Selector                                           ║\033[0m")
                    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
                    print()
                    
                    # Key/Legend
                    print(f"  {DIM}Key:{RESET} 🧠 Thinking  ⚡ Fast  👁️ Vision  💻 Code  🔥 Large  💬 Chat")
                    print()
                    
                    print(f"  {DIM}Fetching models...{RESET}", end="", flush=True)
                    try:
                        models_response = ollama.list()
                        available = models_response.get('models', [])
                        print(f"\r                        \r")
                        
                        if available:
                            print(f"  {DIM}Current:{RESET} {CYAN}{model}{RESET}\n")
                            print(f"  {DIM}#   Model                      Type   Size{RESET}")
                            print(f"  {DIM}─────────────────────────────────────────────────{RESET}")
                            
                            for i, m in enumerate(available, 1):
                                name = m.get('model') or m.get('name') or str(m)
                                size_bytes = m.get('size', 0)
                                size_gb = size_bytes / (1024**3)
                                info = get_model_info(name)
                                
                                is_current = (name == model or model in name)
                                display_name = name[:26] + '..' if len(name) > 28 else name
                                
                                if is_current:
                                    print(f"  {GREEN}{i:<3} {display_name:<28} {info['emoji']:<6}     {size_gb:.1f}GB ◀{RESET}")
                                else:
                                    print(f"  {CYAN}{i:<3}{RESET} {display_name:<28} {info['emoji']:<6}     {DIM}{size_gb:.1f}GB{RESET}")
                            
                            print(f"\n  {GREEN}0{RESET}   ↩️  Back to chat\n")
                            
                            # Prompt for selection
                            try:
                                choice = click.prompt(click.style("  Select", fg="cyan"), default="0", show_default=False).strip()
                                
                                # Exit CLI
                                if choice.lower() in ['/exit', 'exit', '/quit', 'quit']:
                                    print(f"\n{YELLOW}Goodbye!{RESET}\n")
                                    sys.exit(0)
                                
                                if choice == '0' or choice == '':
                                    clear_screen()
                                    print(f"\n  {DIM}Back to chat with {CYAN}{model}{RESET}\n")
                                else:
                                    try:
                                        num = int(choice)
                                        if 1 <= num <= len(available):
                                            m = available[num - 1]
                                            model = m.get('model') or m.get('name') or str(m)
                                            info = get_model_info(model)
                                            history = [{'role': 'system', 'content': system_prompt}]
                                            
                                            clear_screen()
                                            print(f"\n  \033[32m╔══════════════════════════════════════════════════════════════╗\033[0m")
                                            print(f"  \033[32m║  ✓ Model Switched                                            ║\033[0m")
                                            print(f"  \033[32m╚══════════════════════════════════════════════════════════════╝\033[0m")
                                            print()
                                            print(f"  {BOLD}Model:{RESET}  {CYAN}{model}{RESET}")
                                            print(f"  {BOLD}Type:{RESET}   {info['emoji']}")
                                            print(f"  {BOLD}Speed:{RESET}  {DIM}{info['speed']} response times{RESET}")
                                            print()
                                            print(f"  {DIM}Loading model... first message may take 10-30s{RESET}\n")
                                        else:
                                            print(f"\n  {YELLOW}Invalid selection{RESET}\n")
                                    except ValueError:
                                        # Treat as model name
                                        model = choice
                                        history = [{'role': 'system', 'content': system_prompt}]
                                        clear_screen()
                                        print(f"\n  \033[32m╔══════════════════════════════════════════════════════════════╗\033[0m")
                                        print(f"  \033[32m║  ✓ Model Switched                                            ║\033[0m")
                                        print(f"  \033[32m╚══════════════════════════════════════════════════════════════╝\033[0m")
                                        print()
                                        print(f"  {BOLD}Model:{RESET}  {CYAN}{model}{RESET}")
                                        print()
                                        print(f"  {DIM}Loading model... first message may take 10-30s{RESET}\n")
                            except (KeyboardInterrupt, click.Abort):
                                pass
                        else:
                            print(f"  {YELLOW}No models installed.{RESET}")
                            print(f"  {DIM}Run: ollama pull qwen3:4b{RESET}")
                            input("\n  Press Enter to continue...")
                    except Exception as e:
                        print(f"\r  {RED}Could not fetch models: {e}{RESET}")
                        input("\n  Press Enter to continue...")
                    continue
                
                # Save chat command
                if user_input.lower().startswith('/save'):
                    if not history:
                        print(f"\n  {YELLOW}No messages to save yet.{RESET}\n")
                        continue
                    
                    # Generate filename with timestamp
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        filename = parts[1].strip()
                        if not filename.endswith('.md'):
                            filename += '.md'
                    else:
                        filename = f"chat_{timestamp}.md"
                    
                    # Build markdown content
                    content = f"# Chat Export\n\n"
                    content += f"**Model:** {model}\n"
                    content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    content += f"**Messages:** {len(history)}\n\n"
                    content += "---\n\n"
                    
                    for msg in history:
                        role = msg['role']
                        text = msg['content']
                        if role == 'user':
                            content += f"## 🧑 You\n\n{text}\n\n"
                        else:
                            content += f"## 🧙 Wizard\n\n{text}\n\n"
                    
                    # Save file
                    try:
                        save_path = Path.cwd() / filename
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"\n  {GREEN}✓ Chat saved to: {filename}{RESET}")
                        print(f"  {DIM}{save_path}{RESET}\n")
                    except Exception as e:
                        print(f"\n  {YELLOW}Could not save: {e}{RESET}\n")
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
    """Run chat with a Wizard (CrewAI agent)."""
    import click
    import subprocess
    
    clear_screen()
    
    # Styled header box
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🧙 Wizard Chat                                              ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 AI wizard with powers (code, search, files)               │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    /back      → Return to menu                                │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
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
    """Run a Guild (team of wizards)."""
    import click
    
    clear_screen()
    
    # Styled header box
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🏰 Guild Chat                                               ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Run a team of specialized wizards together                │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    Select a guild below to start the workflow                 │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
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
