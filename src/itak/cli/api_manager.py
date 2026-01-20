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
    
    print(f"\n  {BOLD}{CYAN}⚡ API Gateway Manager{RESET}")
    print(f"  {DIM}Manage local services and remote access{RESET}\n")
    
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
    print(f"    {GREEN}[1]{RESET} 📊 {WHITE}Show Service Status{RESET}")
    print()
    print(f"    {GREEN}[2]{RESET} 🌐 {WHITE}Cloudflare Tunnel (Quick){RESET}")
    print(f"        {DIM}Instant public URL, no account needed{RESET}")
    print()
    print(f"    {GREEN}[3]{RESET} 🔒 {WHITE}Cloudflare Tunnel (Permanent){RESET}")
    print(f"        {DIM}Custom domain, requires Cloudflare account{RESET}")
    print()
    print(f"    {GREEN}[4]{RESET} 🖥️  {WHITE}Configure VPS Connection{RESET}")
    print(f"        {DIM}Connect to your own VPS via FRP tunnel{RESET}")
    print()
    print(f"    {GREEN}[5]{RESET} 🚀 {WHITE}Start/Stop FRP Tunnel{RESET}")
    print()
    print(f"    {GREEN}[0]{RESET} ↩️  {WHITE}Back to Main Menu{RESET}")
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
    """Show status of all API services."""
    print(f"\n  {BOLD}📊 Service Status{RESET}\n")
    
    if not check_docker():
        print(f"  {RED}❌ Docker is not running{RESET}\n")
        return
    
    services = [
        ('ollama', 'Ollama LLM', f'http://localhost:{PORTS["ollama"]}'),
        ('chromadb', 'ChromaDB', f'http://localhost:{PORTS["chromadb"]}'),
        ('searxng', 'SearXNG', f'http://localhost:{PORTS["searxng"]}'),
        ('crawl4ai', 'Crawl4AI', 'http://localhost:47836'),
        ('frpc', 'FRP Tunnel', 'VPS Connection'),
        ('cloudflared-tunnel', 'Cloudflare Tunnel', 'Public URL'),
    ]
    
    # Check agent-browser CLI (not Docker)
    import subprocess
    try:
        result = subprocess.run(['agent-browser', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  {GREEN}✅{RESET} Agent Browser CLI: {GREEN}Installed{RESET}")
            print(f"     {DIM}npx agent-browser --help{RESET}")
        else:
            print(f"  {DIM}⬜{RESET} Agent Browser CLI: {DIM}Not installed{RESET}")
            print(f"     {DIM}npm install -g agent-browser{RESET}")
    except FileNotFoundError:
        print(f"  {DIM}⬜{RESET} Agent Browser CLI: {DIM}Not installed{RESET}")
        print(f"     {DIM}npm install -g agent-browser{RESET}")
    
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


def install_cloudflare_temp():
    """Install temporary Cloudflare tunnel (no account needed)."""
    print(f"\n  {CYAN}🌐 Starting Cloudflare Tunnel (Temporary)...{RESET}\n")
    
    if not check_docker():
        print(f"  {YELLOW}⚠️  Docker is not running. Please start Docker first.{RESET}\n")
        return False
    
    DOCKER_DIR.mkdir(parents=True, exist_ok=True)
    
    compose_file = DOCKER_DIR / 'cloudflare-temp.yml'
    compose_file.write_text(CLOUDFLARE_TEMP_COMPOSE)
    
    print(f"  {DIM}Starting tunnel to expose port {PORTS['gateway']}...{RESET}\n")
    
    try:
        subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), 'up', '-d'],
            check=True
        )
        
        import time
        time.sleep(5)
        
        logs = subprocess.run(
            ['docker', 'logs', 'cloudflared-tunnel'],
            capture_output=True, text=True
        )
        
        # Look for the trycloudflare.com URL in logs
        for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
            if 'trycloudflare.com' in line.lower():
                print(f"  {GREEN}✅ Tunnel URL found in logs!{RESET}")
                print(f"  {CYAN}{line.strip()}{RESET}")
                break
        else:
            print(f"  {GREEN}✅ Tunnel started! Check logs for URL:{RESET}")
            print(f"  {DIM}docker logs cloudflared-tunnel{RESET}")
        
        print()
        return True
    except subprocess.CalledProcessError as e:
        print(f"  {YELLOW}⚠️  Failed to start tunnel: {e}{RESET}\n")
        return False


def install_cloudflare_permanent():
    """Install permanent Cloudflare tunnel (requires account)."""
    print(f"\n  {CYAN}🔒 Setting up Cloudflare Tunnel (Permanent)...{RESET}\n")
    
    if not check_docker():
        print(f"  {YELLOW}⚠️  Docker is not running. Please start Docker first.{RESET}\n")
        return False
    
    print(f"  {BOLD}To set up a permanent tunnel:{RESET}")
    print(f"  1. Go to https://one.dash.cloudflare.com/")
    print(f"  2. Navigate to: Zero Trust → Networks → Tunnels")
    print(f"  3. Create a new tunnel")
    print(f"  4. Copy the tunnel token")
    print()
    
    import click
    token = click.prompt(f"  Enter Cloudflare Tunnel Token (or 'skip')", default='skip')
    
    if token.lower() == 'skip':
        print(f"\n  {YELLOW}Skipped. Run this option again when you have a token.{RESET}\n")
        return False
    
    DOCKER_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save token to .env
    env_file = DOCKER_DIR / '.env'
    env_content = f"CLOUDFLARE_TUNNEL_TOKEN={token}\n"
    env_file.write_text(env_content)
    
    compose_file = DOCKER_DIR / 'cloudflare-permanent.yml'
    compose_file.write_text(CLOUDFLARE_PERMANENT_COMPOSE)
    
    print(f"\n  {DIM}Token saved. Starting tunnel...{RESET}")
    
    try:
        subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), '--env-file', str(env_file), 'up', '-d'],
            check=True
        )
        print(f"\n  {GREEN}✅ Permanent tunnel configured!{RESET}")
        print(f"  {DIM}Manage at: https://one.dash.cloudflare.com/{RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  {YELLOW}⚠️  Failed to start tunnel: {e}{RESET}\n")
        return False


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


def toggle_frp_tunnel():
    """Start or stop FRP tunnel."""
    if not check_docker():
        print(f"\n  {YELLOW}⚠️  Docker is not running.{RESET}\n")
        return
    
    # Find the correct compose file
    # Priority 1: Custom frpc.yml in ~/.itak/docker/
    # Priority 2: Main api-gateway docker-compose.yml (with tunnel profile)
    custom_compose = DOCKER_DIR / 'frpc.yml'
    
    # Find main docker-compose.yml (relative to this package)
    package_dir = Path(__file__).parent.parent.parent.parent  # Up to repo root
    main_compose = package_dir / 'docker' / 'api-gateway' / 'docker-compose.yml'
    
    # Also check frpc.toml in same dir as main compose
    main_frpc_config = main_compose.parent / 'frpc.toml'
    
    # Determine which compose to use
    use_main_compose = False
    compose_file = None
    
    if custom_compose.exists():
        compose_file = custom_compose
    elif main_compose.exists() and main_frpc_config.exists():
        compose_file = main_compose
        use_main_compose = True
    else:
        print(f"\n  {YELLOW}FRP not configured.{RESET}")
        print(f"  Use option [4] to configure VPS connection first.\n")
        return
    
    status, _ = get_container_status('frpc')
    
    if status == 'running':
        print(f"\n  {CYAN}Stopping FRP tunnel...{RESET}")
        if use_main_compose:
            subprocess.run(['docker', 'compose', '-f', str(compose_file), '-p', 'api-gateway', '--profile', 'tunnel', 'down', 'frpc'], capture_output=True)
        else:
            subprocess.run(['docker', 'compose', '-f', str(compose_file), 'down'], capture_output=True)
        print(f"  {GREEN}✅ FRP tunnel stopped.{RESET}\n")
    else:
        print(f"\n  {CYAN}Starting FRP tunnel...{RESET}")
        if use_main_compose:
            result = subprocess.run(['docker', 'compose', '-f', str(compose_file), '-p', 'api-gateway', '--profile', 'tunnel', 'up', '-d', 'frpc'], capture_output=True)
        else:
            result = subprocess.run(['docker', 'compose', '-f', str(compose_file), 'up', '-d'], capture_output=True)
        
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
            print(f"  {YELLOW}⚠️  Connection may have issues. Check logs:{RESET}")
            print(f"  {DIM}docker logs frpc{RESET}")
        
        print()


def run_api_menu():
    """Run the API submenu loop."""
    import click
    
    while True:
        print_api_menu()
        
        try:
            choice = click.prompt(
                click.style("  Choice", fg="cyan"),
                type=int,
                default=0
            )
            
            if choice == 0:
                return  # Back to main menu
            elif choice == 1:
                show_service_status()
                click.pause("  Press any key to continue...")
            elif choice == 2:
                install_cloudflare_temp()
                click.pause("  Press any key to continue...")
            elif choice == 3:
                install_cloudflare_permanent()
                click.pause("  Press any key to continue...")
            elif choice == 4:
                configure_vps()
                click.pause("  Press any key to continue...")
            elif choice == 5:
                toggle_frp_tunnel()
                click.pause("  Press any key to continue...")
            else:
                print(f"  {YELLOW}Invalid choice. Please enter 0-5.{RESET}")
                
        except click.Abort:
            return
        except Exception as e:
            print(f"  {YELLOW}Error: {e}{RESET}")


if __name__ == '__main__':
    run_api_menu()
