"""
iTaK API Gateway Manager
Handles FastAPI gateway installation, Cloudflare tunnel, and VPS/FRP setup
"""
import os
import subprocess
import sys
import json
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

# Configuration directory
CONFIG_DIR = Path.home() / '.itak'
DOCKER_DIR = CONFIG_DIR / 'docker'
CONFIG_FILE = CONFIG_DIR / 'api_config.json'

# Default ports (5-digit to avoid conflicts)
PORTS = {
    'gateway': 28934,
    'ollama': 11434,
    'chromadb': 29800,
    'playwright': 39281,
    'searxng': 48192,
    'frp_control': 7000,
}


class ExitCLI(Exception):
    """Raised when user wants to exit the entire CLI."""
    pass


def is_exit_command(text: str) -> bool:
    """Check if the input is an exit command."""
    if text is None:
        return False
    cmd = text.strip().lower()
    return cmd in ['exit', '/exit', '/quit', '/q', 'quit', 'q']


def prompt_with_exit(prompt_text: str, default: str = "0") -> str:
    """Prompt user for input, raising ExitCLI if exit command entered."""
    import click
    result = click.prompt(click.style(prompt_text, fg="cyan"), default=default).strip()
    if is_exit_command(result):
        raise ExitCLI()
    return result

# FRP Client Configuration Template
FRP_CLIENT_CONFIG = '''# FRP Client Configuration
# Connects your local services to your VPS

serverAddr = "{vps_ip}"
serverPort = 7000
auth.method = "token"
auth.token = "{auth_token}"

# Tunnel 1: API Gateway
[[proxies]]
name = "api-gateway"
type = "tcp"
localIP = "127.0.0.1"
localPort = 28934
remotePort = 28934

# Tunnel 2: Ollama LLM
[[proxies]]
name = "ollama"
type = "tcp"
localIP = "host.docker.internal"
localPort = 11434
remotePort = 11434

# Tunnel 3: Playwright Browser
[[proxies]]
name = "playwright"
type = "tcp"
localIP = "127.0.0.1"
localPort = 39281
remotePort = 39281
'''

# Docker Compose for FRP Client
FRP_CLIENT_COMPOSE = '''version: '3.9'

services:
  frpc:
    image: snowdreamtech/frpc
    container_name: frpc
    restart: unless-stopped
    volumes:
      - ./frpc.toml:/etc/frp/frpc.toml
    extra_hosts:
      - "host.docker.internal:host-gateway"
    network_mode: host
'''

# Cloudflare tunnel compose (temporary - no account needed)
CLOUDFLARE_TEMP_COMPOSE = '''version: '3.9'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    command: tunnel --no-autoupdate --url http://host.docker.internal:28934
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"
'''

# Cloudflare tunnel compose (permanent - needs token)
CLOUDFLARE_PERMANENT_COMPOSE = '''version: '3.9'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
    restart: unless-stopped
'''


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_config():
    """Load API configuration from JSON and/or .env file."""
    config = {}
    
    # Load from JSON config
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
        except:
            pass
    
    # Also check .env file for VPS settings
    env_file = Path.cwd() / '.env'
    if env_file.exists():
        try:
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith('VPS_IP=') and not line.startswith('#'):
                    config['vps_ip'] = line.split('=', 1)[1]
                elif line.startswith('FRP_AUTH_TOKEN=') and not line.startswith('#'):
                    config['auth_token'] = line.split('=', 1)[1]
        except:
            pass
    
    return config


def save_config(config):
    """Save API configuration to JSON and update .env file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    
    # Also update .env file
    env_file = Path.cwd() / '.env'
    if env_file.exists():
        try:
            lines = env_file.read_text().splitlines()
            new_lines = []
            vps_written = False
            token_written = False
            
            for line in lines:
                # Update existing VPS_IP line
                if line.strip().startswith('VPS_IP=') or line.strip().startswith('# VPS_IP='):
                    if config.get('vps_ip'):
                        new_lines.append(f"VPS_IP={config['vps_ip']}")
                        vps_written = True
                    else:
                        new_lines.append(line)
                # Update existing FRP_AUTH_TOKEN line
                elif line.strip().startswith('FRP_AUTH_TOKEN=') or line.strip().startswith('# FRP_AUTH_TOKEN='):
                    if config.get('auth_token'):
                        new_lines.append(f"FRP_AUTH_TOKEN={config['auth_token']}")
                        token_written = True
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Append if not found
            if config.get('vps_ip') and not vps_written:
                new_lines.append(f"VPS_IP={config['vps_ip']}")
            if config.get('auth_token') and not token_written:
                new_lines.append(f"FRP_AUTH_TOKEN={config['auth_token']}")
            
            env_file.write_text('\n'.join(new_lines) + '\n')
        except:
            pass


def print_api_menu():
    """Print the API submenu."""
    clear_screen()
    config = load_config()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║\033[0m  ⚡ {BOLD}API Gateway Manager{RESET}                                     \033[35m║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 What can you do?                                          │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    🔗 Tunnels     → Cloudflare or FRP to expose local APIs    │\033[0m")
    print(f"  \033[90m│    🌐 VPS         → Connect to your remote server             │\033[0m")
    print(f"  \033[90m│    📊 Status      → Check all services and ports              │\033[0m")
    print(f"  \033[90m│    🧩 Services    → Supabase, ComfyUI, SearXNG, etc.          │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    # Show current endpoints
    print(f"  {BOLD}Local Endpoints:{RESET}")
    print(f"    • API Gateway:  {CYAN}http://localhost:{PORTS['gateway']}{RESET}")
    print(f"    • Ollama:       {CYAN}http://localhost:{PORTS['ollama']}{RESET}")
    print(f"    • ChromaDB:     {CYAN}http://localhost:{PORTS['chromadb']}{RESET}")
    print(f"    • Playwright:   {CYAN}ws://localhost:{PORTS['playwright']}{RESET}")
    print(f"    • SearXNG:      {CYAN}http://localhost:{PORTS['searxng']}{RESET}")
    
    if config.get('vps_ip'):
        print(f"\n  {BOLD}VPS Endpoints:{RESET} {GREEN}(Connected){RESET}")
        vps = config['vps_ip']
        print(f"    • API Gateway:  {CYAN}http://{vps}:{PORTS['gateway']}{RESET}")
        print(f"    • Ollama:       {CYAN}http://{vps}:{PORTS['ollama']}{RESET}")
        print(f"    • Playwright:   {CYAN}ws://{vps}:{PORTS['playwright']}{RESET}")
    
    print(f"\n  {BOLD}Options:{RESET}")
    print(f"    {GREEN}[1]{RESET} 📊 {WHITE}Service Status{RESET}")
    print(f"    {GREEN}[2]{RESET} 🌐 {WHITE}Cloudflare Tunnels{RESET}")
    print(f"    {GREEN}[3]{RESET} 🚀 {WHITE}VPS / FRP Tunnel{RESET}")
    print(f"    {GREEN}[4]{RESET} 🧩 {WHITE}Optional Services{RESET}  {DIM}Supabase, ComfyUI, etc{RESET}")
    print()
    print(f"    {GREEN}[0]{RESET} ↩️  {WHITE}Back{RESET}")
    print()


def check_docker():
    """Check if Docker is running."""
    try:
        subprocess.run(['docker', 'info'], capture_output=True, check=True)
        return True
    except:
        return False


def get_container_status(name):
    """Get status of a Docker container."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f'name={name}', '--format', '{{.Status}}'],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        if 'Up' in status:
            return 'running', status
        elif status:
            return 'stopped', status
        return 'not_found', None
    except:
        return 'error', None


def show_service_status():
    """Show status of all API services with install options."""
    import click
    
    while True:
        clear_screen()
        print(f"\n  {BOLD}📊 Service Status{RESET}\n")
        
        if not check_docker():
            print(f"  {RED}❌ Docker is not running{RESET}\n")
            input("  Press Enter to go back...")
            return
        
        # Track not-installed items for install menu
        not_installed = []
        
        # Check agent-browser CLI (not Docker)
        agent_browser_installed = False
        try:
            result = subprocess.run(['agent-browser', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  {GREEN}✅{RESET} Agent Browser CLI: {GREEN}Installed{RESET}")
                agent_browser_installed = True
            else:
                print(f"  {DIM}⬜{RESET} Agent Browser CLI: {DIM}Not installed{RESET}")
                not_installed.append(('agent-browser', 'Agent Browser CLI'))
        except FileNotFoundError:
            print(f"  {DIM}⬜{RESET} Agent Browser CLI: {DIM}Not installed{RESET}")
            not_installed.append(('agent-browser', 'Agent Browser CLI'))
        
        services = [
            ('ollama', 'Ollama LLM', f'http://localhost:{PORTS["ollama"]}'),
            ('chromadb', 'ChromaDB', f'http://localhost:{PORTS["chromadb"]}'),
            ('searxng', 'SearXNG', f'http://localhost:{PORTS["searxng"]}'),
            ('crawl4ai', 'Crawl4AI', 'http://localhost:47836'),
            ('frpc', 'FRP Tunnel', 'VPS Connection'),
            ('cloudflared-tunnel', 'Cloudflare Tunnel', 'Public URL'),
        ]
        
        for container, name, url in services:
            status, details = get_container_status(container)
            
            if status == 'running':
                print(f"  {GREEN}✅{RESET} {name}: {GREEN}Running{RESET}")
                print(f"     {DIM}{url}{RESET}")
            elif status == 'stopped':
                print(f"  {YELLOW}⏸️{RESET}  {name}: {YELLOW}Stopped{RESET}")
            else:
                print(f"  {DIM}⬜{RESET} {name}: {DIM}Not installed{RESET}")
        
        print()
        
        # Show install options if there are missing services
        if not_installed:
            print(f"  {BOLD}Install Missing:{RESET}")
            for idx, (key, name) in enumerate(not_installed, 1):
                print(f"    {GREEN}[{idx}]{RESET} Install {name}")
            print()
        
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if is_exit_command(choice):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(not_installed):
                    key, name = not_installed[choice_num - 1]
                    
                    if key == 'agent-browser':
                        print(f"\n  {CYAN}Installing {name}...{RESET}")
                        print(f"  {DIM}This may take a minute...{RESET}\n")
                        
                        result = subprocess.run(['npm', 'install', '-g', 'agent-browser'], 
                            capture_output=False)
                        
                        if result.returncode == 0:
                            print(f"\n  {GREEN}✅ {name} installed!{RESET}")
                            # Try to install Chromium
                            print(f"\n  {CYAN}Installing Chromium browser...{RESET}")
                            subprocess.run(['npx', 'agent-browser', 'install'], capture_output=False)
                        else:
                            print(f"\n  {YELLOW}⚠️  Installation may have issues. Check above for errors.{RESET}")
                        
                        input("\n  Press Enter to continue...")
                else:
                    print(f"  {YELLOW}Invalid choice{RESET}")
            except ValueError:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return


def cloudflare_menu():
    """Combined Cloudflare Tunnel submenu with Quick and Permanent options."""
    import click
    
    if not check_docker():
        print(f"\n  {YELLOW}⚠️  Docker is not running.{RESET}\n")
        return
    
    while True:
        # Get current status
        status, _ = get_container_status('cloudflared-tunnel')
        is_running = status == 'running'
        
        # Check tunnel type
        config = load_config()
        has_permanent_token = bool(config.get('cloudflare_token', ''))
        
        # Try to detect if it's Quick or Permanent
        tunnel_type = "Unknown"
        current_url = None
        if is_running:
            try:
                logs = subprocess.run(['docker', 'logs', 'cloudflared-tunnel', '--tail', '50'],
                    capture_output=True, text=True)
                for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
                    if 'trycloudflare.com' in line.lower():
                        tunnel_type = "Quick (Temporary)"
                        import re
                        match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                        if match:
                            current_url = match.group(0)
                        break
                else:
                    tunnel_type = "Permanent"
            except:
                pass
        
        # Show submenu
        clear_screen()
        print(f"\n  {BOLD}🌐 Cloudflare Tunnels{RESET}")
        print(f"  {CYAN}https://one.dash.cloudflare.com/{RESET}")
        print()
        
        # Show status
        if is_running:
            print(f"  Status: {GREEN}● Running ({tunnel_type}){RESET}")
            if current_url:
                print(f"  URL: {CYAN}{current_url}{RESET}")
        else:
            print(f"  Status: {DIM}○ Stopped{RESET}")
        
        print()
        print(f"  {GREEN}[1]{RESET} 🌐 Quick Tunnel")
        print(f"      {DIM}Instant URL, no account needed{RESET}")
        print(f"      {YELLOW}⚠️  URL changes on restart{RESET}")
        print()
        print(f"  {GREEN}[2]{RESET} 🔒 Permanent Tunnel")
        print(f"      {DIM}Custom domain, requires CF account{RESET}")
        print(f"      {GREEN}✓ Persistent URL{RESET}")
        print()
        if is_running:
            print(f"  {GREEN}[3]{RESET} ⏹️  Stop Current Tunnel")
            print()
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if is_exit_command(choice):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                # Quick Tunnel submenu
                cloudflare_temp_menu()
            
            elif choice == '2':
                # Permanent Tunnel submenu
                cloudflare_permanent_menu()
            
            elif choice == '3' and is_running:
                # Stop current tunnel
                print(f"\n  {CYAN}Stopping Cloudflare tunnel...{RESET}")
                subprocess.run(['docker', 'stop', 'cloudflared-tunnel'], capture_output=True)
                subprocess.run(['docker', 'rm', 'cloudflared-tunnel'], capture_output=True)
                
                new_status, _ = get_container_status('cloudflared-tunnel')
                if new_status != 'running':
                    print(f"  {GREEN}✅ Tunnel stopped.{RESET}")
                else:
                    print(f"  {YELLOW}⚠️  Failed to stop.{RESET}")
                
                input("\n  Press Enter to continue...")
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return


def cloudflare_temp_menu():
    """Cloudflare Quick Tunnel submenu with status and start/stop options."""
    import click
    
    if not check_docker():
        print(f"\n  {YELLOW}⚠️  Docker is not running.{RESET}\n")
        return
    
    DOCKER_DIR.mkdir(parents=True, exist_ok=True)
    compose_file = DOCKER_DIR / 'cloudflare-temp.yml'
    
    while True:
        # Get current status
        status, _ = get_container_status('cloudflared-tunnel')
        is_running = status == 'running'
        
        # Get current URL if running
        current_url = None
        if is_running:
            try:
                logs = subprocess.run(['docker', 'logs', 'cloudflared-tunnel', '--tail', '50'],
                    capture_output=True, text=True)
                for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
                    if 'trycloudflare.com' in line.lower():
                        import re
                        match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                        if match:
                            current_url = match.group(0)
                            break
            except:
                pass
        
        # Show submenu
        clear_screen()
        print(f"\n  {BOLD}🌐 Cloudflare Quick Tunnel{RESET}")
        print()
        
        # Warning about temporary URL
        print(f"  {YELLOW}⚠️  TEMPORARY URL - Changes every restart!{RESET}")
        print(f"  {DIM}No account needed, but URL is not persistent.{RESET}")
        print()
        
        # Show status
        if is_running:
            print(f"  Status: {GREEN}● Running{RESET}")
            if current_url:
                print(f"  URL: {CYAN}{current_url}{RESET}")
            else:
                print(f"  URL: {DIM}Check logs: docker logs cloudflared-tunnel{RESET}")
        else:
            print(f"  Status: {DIM}○ Stopped{RESET}")
        
        print()
        print(f"  {GREEN}[1]{RESET} ▶️  Start Tunnel")
        print(f"  {GREEN}[2]{RESET} ⏹️  Stop Tunnel")
        print(f"  {GREEN}[3]{RESET} 📋 Show Tunnel URL")
        print()
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if is_exit_command(choice):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                # Start
                if is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is already running!{RESET}")
                    if current_url:
                        print(f"  URL: {CYAN}{current_url}{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Starting Cloudflare Quick Tunnel...{RESET}")
                compose_file.write_text(CLOUDFLARE_TEMP_COMPOSE)
                
                subprocess.run(['docker', 'compose', '-f', str(compose_file), 'up', '-d'], capture_output=True)
                
                import time
                time.sleep(5)
                
                # Try to get URL
                logs = subprocess.run(['docker', 'logs', 'cloudflared-tunnel'], capture_output=True, text=True)
                found_url = None
                for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
                    if 'trycloudflare.com' in line.lower():
                        import re
                        match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                        if match:
                            found_url = match.group(0)
                            break
                
                if found_url:
                    print(f"  {GREEN}✅ Tunnel started!{RESET}")
                    print(f"\n  {BOLD}Your public URL:{RESET}")
                    print(f"  {CYAN}{found_url}{RESET}")
                    print(f"\n  {YELLOW}⚠️  This URL will change when tunnel restarts!{RESET}")
                else:
                    print(f"  {GREEN}✅ Tunnel started! Check logs for URL:{RESET}")
                    print(f"  {DIM}docker logs cloudflared-tunnel{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '2':
                # Stop
                if not is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is not running.{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Stopping Cloudflare tunnel...{RESET}")
                subprocess.run(['docker', 'stop', 'cloudflared-tunnel'], capture_output=True)
                subprocess.run(['docker', 'rm', 'cloudflared-tunnel'], capture_output=True)
                
                new_status, _ = get_container_status('cloudflared-tunnel')
                if new_status != 'running':
                    print(f"  {GREEN}✅ Tunnel stopped.{RESET}")
                else:
                    print(f"  {YELLOW}⚠️  Failed to stop. Try: docker stop cloudflared-tunnel{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '3':
                # Show URL
                if not is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is not running. Start it first.{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Fetching tunnel URL...{RESET}")
                logs = subprocess.run(['docker', 'logs', 'cloudflared-tunnel', '--tail', '100'],
                    capture_output=True, text=True)
                
                found = False
                for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
                    if 'trycloudflare.com' in line.lower():
                        print(f"  {CYAN}{line.strip()}{RESET}")
                        found = True
                
                if not found:
                    print(f"  {YELLOW}URL not found in logs. Tunnel may still be starting...{RESET}")
                
                input("\n  Press Enter to continue...")
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return


def cloudflare_permanent_menu():
    """Cloudflare Permanent Tunnel submenu with status, start/stop, and token config."""
    import click
    
    if not check_docker():
        print(f"\n  {YELLOW}⚠️  Docker is not running.{RESET}\n")
        return
    
    DOCKER_DIR.mkdir(parents=True, exist_ok=True)
    compose_file = DOCKER_DIR / 'cloudflare-permanent.yml'
    env_file = DOCKER_DIR / '.env'
    
    while True:
        # Get current status
        status, _ = get_container_status('cloudflared-tunnel')
        is_running = status == 'running'
        
        # Check if token is configured
        config = load_config()
        current_token = config.get('cloudflare_token', '')
        has_token = bool(current_token)
        masked_token = current_token[:12] + '...' if len(current_token) > 12 else (current_token or 'Not set')
        
        # Show submenu
        clear_screen()
        print(f"\n  {BOLD}🔒 Cloudflare Permanent Tunnel{RESET}")
        print()
        
        # Info about permanent tunnel
        print(f"  {GREEN}✓ Persistent URL with custom domain{RESET}")
        print(f"  {DIM}Requires Cloudflare account & tunnel token{RESET}")
        print(f"  {CYAN}https://one.dash.cloudflare.com/{RESET}")
        print()
        
        # Show status
        if is_running:
            print(f"  Status: {GREEN}● Running{RESET}")
        else:
            print(f"  Status: {DIM}○ Stopped{RESET}")
        
        if not has_token:
            print(f"  {YELLOW}⚠️  No token configured{RESET}")
        
        print()
        print(f"  {GREEN}[1]{RESET} ▶️  Start Tunnel")
        print(f"  {GREEN}[2]{RESET} ⏹️  Stop Tunnel")
        print()
        print(f"  {GREEN}[3]{RESET} 🔑 Set Tunnel Token  {DIM}({masked_token}){RESET}")
        print(f"  {GREEN}[4]{RESET} 📖 Setup Instructions")
        print()
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if is_exit_command(choice):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                # Start
                if is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is already running!{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                if not has_token:
                    print(f"\n  {YELLOW}⚠️  No token configured. Use option [3] first.{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Starting Cloudflare Permanent Tunnel...{RESET}")
                
                # Write compose and env files
                compose_file.write_text(CLOUDFLARE_PERMANENT_COMPOSE)
                env_file.write_text(f"CLOUDFLARE_TUNNEL_TOKEN={current_token}\n")
                
                result = subprocess.run(
                    ['docker', 'compose', '-f', str(compose_file), '--env-file', str(env_file), 'up', '-d'],
                    capture_output=True
                )
                
                import time
                time.sleep(3)
                
                new_status, _ = get_container_status('cloudflared-tunnel')
                if new_status == 'running':
                    print(f"  {GREEN}✅ Tunnel started!{RESET}")
                    print(f"  {DIM}Manage at: https://one.dash.cloudflare.com/{RESET}")
                else:
                    print(f"  {YELLOW}⚠️  Failed to start. Check: docker logs cloudflared-tunnel{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '2':
                # Stop
                if not is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is not running.{RESET}")
                    input("\n  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Stopping Cloudflare tunnel...{RESET}")
                subprocess.run(['docker', 'stop', 'cloudflared-tunnel'], capture_output=True)
                subprocess.run(['docker', 'rm', 'cloudflared-tunnel'], capture_output=True)
                
                new_status, _ = get_container_status('cloudflared-tunnel')
                if new_status != 'running':
                    print(f"  {GREEN}✅ Tunnel stopped.{RESET}")
                else:
                    print(f"  {YELLOW}⚠️  Failed to stop. Try: docker stop cloudflared-tunnel{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '3':
                # Set Token
                print(f"\n  Current Token: {CYAN}{masked_token}{RESET}")
                print()
                print(f"  {DIM}Get your token from:{RESET}")
                print(f"  {CYAN}https://one.dash.cloudflare.com/{RESET}")
                print(f"  {DIM}Zero Trust → Networks → Tunnels → Your Tunnel → Configure{RESET}")
                print()
                
                new_token = click.prompt(click.style("  New Token", fg="cyan"), default='').strip()
                
                if new_token:
                    config['cloudflare_token'] = new_token
                    save_config(config)
                    print(f"  {GREEN}✅ Token saved!{RESET}")
                    if is_running:
                        print(f"  {DIM}Restart tunnel to apply changes{RESET}")
                else:
                    print(f"  {YELLOW}No change made{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '4':
                # Setup Instructions
                print(f"\n  {BOLD}How to set up a Cloudflare Tunnel:{RESET}")
                print()
                print(f"  1. Go to {CYAN}https://one.dash.cloudflare.com/{RESET}")
                print(f"  2. Navigate to: Zero Trust → Networks → Tunnels")
                print(f"  3. Click 'Create a tunnel'")
                print(f"  4. Name your tunnel (e.g., 'itak-tunnel')")
                print(f"  5. Choose 'Cloudflared' connector")
                print(f"  6. Copy the tunnel token")
                print(f"  7. Use option [3] here to save the token")
                print(f"  8. Configure public hostname in Cloudflare dashboard")
                print()
                
                input("  Press Enter to continue...")
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return


def configure_vps():
    """Configure VPS connection via FRP."""
    print(f"\n  {CYAN}🖥️  Configure VPS Connection{RESET}\n")
    
    config = load_config()
    
    print(f"  {BOLD}Prerequisites:{RESET}")
    print(f"  1. VPS with FRP server running (see docs/VPS_SETUP.md)")
    print(f"  2. Your auth token from the VPS frps.toml file")
    print()
    print(f"  {DIM}Don't have a token yet? Generate one with:{RESET}")
    print(f"    {CYAN}openssl rand -hex 16{RESET}")
    print(f"  {DIM}Use the SAME token on your VPS and here.{RESET}\n")
    
    import click
    
    vps_ip = click.prompt(
        f"  VPS IP Address",
        default=config.get('vps_ip', '')
    )
    
    if not vps_ip:
        print(f"\n  {YELLOW}Cancelled.{RESET}\n")
        return
    
    print(f"\n  {DIM}Enter the auth token from your VPS frps.toml file:{RESET}")
    auth_token = click.prompt(
        f"  FRP Auth Token",
        default=config.get('auth_token', ''),
        show_default=False
    )
    
    if not auth_token:
        print(f"\n  {YELLOW}Auth token is required. Get it from your VPS frps.toml.{RESET}\n")
        return
    
    # Save config
    config['vps_ip'] = vps_ip
    config['auth_token'] = auth_token
    save_config(config)
    
    # Generate FRP client config
    DOCKER_DIR.mkdir(parents=True, exist_ok=True)
    
    frpc_config = FRP_CLIENT_CONFIG.format(vps_ip=vps_ip, auth_token=auth_token)
    frpc_file = DOCKER_DIR / 'frpc.toml'
    frpc_file.write_text(frpc_config)
    
    compose_file = DOCKER_DIR / 'frpc.yml'
    compose_file.write_text(FRP_CLIENT_COMPOSE)
    
    print(f"\n  {GREEN}✅ VPS configuration saved!{RESET}")
    print(f"  {DIM}Config: {frpc_file}{RESET}")
    print(f"\n  Use option [5] to start the FRP tunnel.\n")


def frp_tunnel_menu():
    """FRP Tunnel submenu with status and start/stop options."""
    import click
    
    if not check_docker():
        print(f"\n  {YELLOW}⚠️  Docker is not running.{RESET}\n")
        return
    
    # Find compose file configuration
    custom_compose = DOCKER_DIR / 'frpc.yml'
    package_dir = Path(__file__).parent.parent.parent.parent
    main_compose = package_dir / 'docker' / 'api-gateway' / 'docker-compose.yml'
    main_frpc_config = main_compose.parent / 'frpc.toml'
    
    use_main_compose = False
    compose_file = None
    configured = False
    
    if custom_compose.exists():
        compose_file = custom_compose
        configured = True
    elif main_compose.exists() and main_frpc_config.exists():
        compose_file = main_compose
        use_main_compose = True
        configured = True
    
    while True:
        # Get current status
        status, _ = get_container_status('frpc')
        is_running = status == 'running'
        
        # Show submenu
        clear_screen()
        print(f"\n  {BOLD}🚀 VPS / FRP Tunnel{RESET}")
        print(f"  {DIM}Connect local services to your VPS{RESET}")
        print(f"  {CYAN}https://github.com/fatedier/frp{RESET}")
        print()
        
        # Show status
        if is_running:
            config = load_config()
            vps = config.get('vps_ip', 'VPS')
            print(f"  Status: {GREEN}● Running{RESET}")
            print(f"  VPS: {CYAN}{vps}{RESET}")
        else:
            print(f"  Status: {DIM}○ Stopped{RESET}")
        
        if not configured:
            print(f"  {YELLOW}⚠️  Not configured - use option [5] for setup guide{RESET}")
        
        # Show current config
        config = load_config()
        current_ip = config.get('vps_ip', 'Not set')
        current_token = config.get('frp_token', 'Not set')
        if current_token != 'Not set':
            current_token = current_token[:8] + '...' if len(current_token) > 8 else current_token
        
        print()
        print(f"  {GREEN}[1]{RESET} ▶️  Start Tunnel")
        print(f"  {GREEN}[2]{RESET} ⏹️  Stop Tunnel")
        print()
        print(f"  {GREEN}[3]{RESET} 🌐 Change VPS IP     {DIM}({current_ip}){RESET}")
        print(f"  {GREEN}[4]{RESET} 🔑 Change FRP Token  {DIM}({current_token}){RESET}")
        print(f"  {GREEN}[5]{RESET} 📖 Setup Instructions")
        print()
        print(f"  {GREEN}[0]{RESET} ↩️  Back")
        print()
        
        try:
            choice = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            if is_exit_command(choice):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            if choice == '0' or choice == '':
                return
            
            elif choice == '1':
                # Start
                if is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is already running!{RESET}")
                    input("  Press Enter to continue...")
                    continue
                
                if not configured:
                    print(f"\n  {YELLOW}⚠️  VPS not configured. Use option [4] first.{RESET}")
                    input("  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Starting FRP tunnel...{RESET}")
                if use_main_compose:
                    subprocess.run(['docker', 'compose', '-f', str(compose_file), '-p', 'api-gateway', '--profile', 'tunnel', 'up', '-d', 'frpc'], capture_output=True)
                else:
                    subprocess.run(['docker', 'compose', '-f', str(compose_file), 'up', '-d'], capture_output=True)
                
                import time
                time.sleep(2)
                
                logs = subprocess.run(['docker', 'logs', 'frpc', '--tail', '10'], capture_output=True, text=True)
                
                if 'start proxy success' in logs.stdout or 'start proxy success' in logs.stderr:
                    print(f"  {GREEN}✅ FRP tunnel connected!{RESET}")
                    config = load_config()
                    vps = config.get('vps_ip', 'your-vps-ip')
                    print(f"\n  {BOLD}Your VPS endpoints:{RESET}")
                    print(f"    • API:      http://{vps}:{PORTS['gateway']}")
                    print(f"    • Ollama:   http://{vps}:{PORTS['ollama']}")
                    print(f"    • Playwright: ws://{vps}:{PORTS['playwright']}")
                else:
                    new_status, _ = get_container_status('frpc')
                    if new_status == 'running':
                        print(f"  {GREEN}✅ Tunnel started (checking connection...){RESET}")
                    else:
                        print(f"  {YELLOW}⚠️  Failed to start. Check: docker logs frpc{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '2':
                # Stop
                if not is_running:
                    print(f"\n  {YELLOW}ℹ️  Tunnel is not running.{RESET}")
                    input("  Press Enter to continue...")
                    continue
                
                print(f"\n  {CYAN}Stopping FRP tunnel...{RESET}")
                subprocess.run(['docker', 'stop', 'frpc'], capture_output=True)
                subprocess.run(['docker', 'rm', 'frpc'], capture_output=True)
                
                new_status, _ = get_container_status('frpc')
                if new_status != 'running':
                    print(f"  {GREEN}✅ FRP tunnel stopped.{RESET}")
                else:
                    print(f"  {YELLOW}⚠️  Failed to stop. Try: docker stop frpc{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '3':
                # Change VPS IP
                config = load_config()
                current = config.get('vps_ip', '')
                print(f"\n  Current VPS IP: {CYAN}{current or 'Not set'}{RESET}")
                new_ip = click.prompt(click.style("  New VPS IP", fg="cyan"), default=current or '').strip()
                
                if new_ip:
                    config['vps_ip'] = new_ip
                    save_config(config)
                    print(f"  {GREEN}✅ VPS IP updated to: {new_ip}{RESET}")
                    
                    # Update frpc.toml if it exists
                    main_frpc = package_dir / 'docker' / 'api-gateway' / 'frpc.toml'
                    if main_frpc.exists():
                        print(f"  {DIM}Note: Restart tunnel to apply changes{RESET}")
                else:
                    print(f"  {YELLOW}No change made{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '4':
                # Change FRP Token
                config = load_config()
                current = config.get('frp_token', '')
                masked = current[:8] + '...' if current and len(current) > 8 else (current or 'Not set')
                print(f"\n  Current FRP Token: {CYAN}{masked}{RESET}")
                new_token = click.prompt(click.style("  New FRP Token", fg="cyan"), default='').strip()
                
                if new_token:
                    config['frp_token'] = new_token
                    save_config(config)
                    print(f"  {GREEN}✅ FRP Token updated{RESET}")
                    
                    # Update frpc.toml with new token
                    main_frpc = package_dir / 'docker' / 'api-gateway' / 'frpc.toml'
                    if main_frpc.exists():
                        try:
                            content = main_frpc.read_text()
                            import re
                            content = re.sub(r'auth\.token\s*=\s*"[^"]*"', f'auth.token = "{new_token}"', content)
                            main_frpc.write_text(content)
                            print(f"  {GREEN}✅ frpc.toml updated{RESET}")
                            print(f"  {DIM}Restart tunnel to apply changes{RESET}")
                        except Exception as e:
                            print(f"  {YELLOW}⚠️  Could not update frpc.toml: {e}{RESET}")
                else:
                    print(f"  {YELLOW}No change made{RESET}")
                
                input("\n  Press Enter to continue...")
            
            elif choice == '5':
                # Setup Instructions
                print(f"\n  {BOLD}How to set up FRP Tunnel to your VPS:{RESET}")
                print()
                print(f"  {BOLD}1. Install FRP on your VPS:{RESET}")
                print(f"     {CYAN}https://github.com/fatedier/frp/releases{RESET}")
                print()
                print(f"  {BOLD}2. Create frps.toml on VPS:{RESET}")
                print(f"     bindPort = 7000")
                print(f"     auth.token = \"your-secret-token\"")
                print()
                print(f"  {BOLD}3. Run FRP server on VPS:{RESET}")
                print(f"     ./frps -c frps.toml")
                print()
                print(f"  {BOLD}4. Configure here:{RESET}")
                print(f"     Use option [3] to set your VPS IP")
                print(f"     Use option [4] to set the same token")
                print()
                print(f"  {BOLD}5. Start tunnel:{RESET}")
                print(f"     Use option [1] to connect")
                print()
                print(f"  {DIM}Full guide: https://github.com/fatedier/frp{RESET}")
                print()
                
                input("  Press Enter to continue...")
            
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except KeyboardInterrupt:
            return


def run_api_menu():
    """Run the API submenu loop."""
    import click
    
    while True:
        print_api_menu()
        
        try:
            raw = click.prompt(click.style("  Choice", fg="cyan"), default="0").strip()
            
            # Check for exit command
            if is_exit_command(raw):
                print(f"\n{YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)
            
            try:
                choice = int(raw)
            except ValueError:
                print(f"  {YELLOW}Invalid choice. Please enter 0-4.{RESET}")
                continue
            
            if choice == 0:
                return  # Back to main menu
            elif choice == 1:
                show_service_status()
                # No pause needed - submenu handles its own flow
            elif choice == 2:
                cloudflare_menu()
                # No pause needed - submenu handles its own flow
            elif choice == 3:
                frp_tunnel_menu()
                # No pause needed - submenu handles its own flow
            elif choice == 4:
                # Optional Services
                try:
                    from .optional_services import run_optional_services_menu
                    run_optional_services_menu()
                except ImportError:
                    print(f"  {YELLOW}Optional Services module not available.{RESET}")
                    click.pause("  Press any key to continue...")
                except Exception as e:
                    print(f"  {YELLOW}Error: {e}{RESET}")
                    click.pause("  Press any key to continue...")
            else:
                print(f"  {YELLOW}Invalid choice. Please enter 0-4.{RESET}")
                
        except click.Abort:
            return
        except ExitCLI:
            print(f"\n{YELLOW}Goodbye!{RESET}\n")
            sys.exit(0)
        except Exception as e:
            print(f"  {YELLOW}Error: {e}{RESET}")


if __name__ == '__main__':
    run_api_menu()
