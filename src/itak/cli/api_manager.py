"""
iTaK API Gateway Manager
Handles FastAPI gateway installation and Cloudflare tunnel setup
"""
import os
import subprocess
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

# Docker compose for FastAPI gateway
FASTAPI_COMPOSE = '''version: '3.9'

services:
  itak-gateway:
    image: python:3.11-slim
    container_name: itak-gateway
    working_dir: /app
    command: >
      bash -c "pip install fastapi uvicorn httpx && 
               python -c \\"
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='iTaK API Gateway')

@app.get('/')
def root():
    return {'status': 'ok', 'message': 'iTaK Gateway Running'}

@app.get('/health')
def health():
    return {'healthy': True}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
\\""
    ports:
      - "8080:8080"
    restart: unless-stopped
    networks:
      - itak-network

networks:
  itak-network:
    driver: bridge
'''

# Cloudflare tunnel compose (temporary - no account needed)
CLOUDFLARE_TEMP_COMPOSE = '''version: '3.9'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    command: tunnel --no-autoupdate --url http://host.docker.internal:8080
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


def print_api_menu():
    """Print the API submenu."""
    clear_screen()
    print(f"\n  {BOLD}{CYAN}⚡ API Gateway Manager{RESET}")
    print(f"  {DIM}Setup FastAPI gateway and remote access tunnels{RESET}\n")
    
    print(f"  {BOLD}Services:{RESET}")
    print(f"    {GREEN}[1]{RESET} 🚀 {WHITE}Install FastAPI Gateway{RESET}")
    print(f"        {DIM}Local API gateway on port 8080{RESET}")
    print()
    print(f"    {GREEN}[2]{RESET} 🌐 {WHITE}Cloudflare Tunnel (Temporary){RESET}")
    print(f"        {DIM}Quick public URL, no account needed{RESET}")
    print()
    print(f"    {GREEN}[3]{RESET} 🔒 {WHITE}Cloudflare Tunnel (Permanent){RESET}")
    print(f"        {DIM}Custom domain, requires Cloudflare account{RESET}")
    print()
    print(f"  {BOLD}Status:{RESET}")
    print(f"    {GREEN}[4]{RESET} 📊 {WHITE}Show Service Status{RESET}")
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


def install_fastapi_gateway():
    """Install the FastAPI gateway container."""
    print(f"\n  {CYAN}📦 Installing FastAPI Gateway...{RESET}\n")
    
    if not check_docker():
        print(f"  {YELLOW}⚠️  Docker is not running. Please start Docker first.{RESET}\n")
        return False
    
    # Create compose directory
    compose_dir = Path.home() / '.itak' / 'docker'
    compose_dir.mkdir(parents=True, exist_ok=True)
    
    compose_file = compose_dir / 'fastapi-gateway.yml'
    compose_file.write_text(FASTAPI_COMPOSE)
    
    print(f"  Created: {compose_file}")
    
    try:
        subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), 'up', '-d'],
            check=True
        )
        print(f"\n  {GREEN}✅ FastAPI Gateway installed!{RESET}")
        print(f"  {DIM}Access at: http://localhost:8080{RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  {YELLOW}⚠️  Failed to start gateway: {e}{RESET}\n")
        return False


def install_cloudflare_temp():
    """Install temporary Cloudflare tunnel (no account needed)."""
    print(f"\n  {CYAN}🌐 Setting up Cloudflare Tunnel (Temporary)...{RESET}\n")
    
    if not check_docker():
        print(f"  {YELLOW}⚠️  Docker is not running. Please start Docker first.{RESET}\n")
        return False
    
    # Check if gateway is running
    status, _ = get_container_status('itak-gateway')
    if status != 'running':
        print(f"  {YELLOW}⚠️  FastAPI Gateway not running. Install it first (Option 1).{RESET}\n")
        return False
    
    compose_dir = Path.home() / '.itak' / 'docker'
    compose_dir.mkdir(parents=True, exist_ok=True)
    
    compose_file = compose_dir / 'cloudflare-temp.yml'
    compose_file.write_text(CLOUDFLARE_TEMP_COMPOSE)
    
    print(f"  Created: {compose_file}")
    print(f"  {DIM}Starting tunnel to expose port 8080...{RESET}\n")
    
    try:
        # Start the tunnel
        result = subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), 'up', '-d'],
            check=True
        )
        
        # Wait a moment and get the URL
        import time
        time.sleep(3)
        
        logs = subprocess.run(
            ['docker', 'logs', 'cloudflared-tunnel'],
            capture_output=True, text=True
        )
        
        # Look for the trycloudflare.com URL in logs
        for line in logs.stdout.split('\n') + logs.stderr.split('\n'):
            if 'trycloudflare.com' in line or '.cloudflare' in line:
                print(f"  {GREEN}✅ Tunnel URL: {line.strip()}{RESET}")
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
    
    compose_dir = Path.home() / '.itak' / 'docker'
    compose_dir.mkdir(parents=True, exist_ok=True)
    
    # Save token to .env
    env_file = compose_dir / '.env'
    env_content = f"CLOUDFLARE_TUNNEL_TOKEN={token}\n"
    env_file.write_text(env_content)
    
    compose_file = compose_dir / 'cloudflare-permanent.yml'
    compose_file.write_text(CLOUDFLARE_PERMANENT_COMPOSE)
    
    print(f"\n  Created: {compose_file}")
    print(f"  Token saved to: {env_file}")
    
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


def show_service_status():
    """Show status of all API services."""
    print(f"\n  {BOLD}📊 Service Status{RESET}\n")
    
    services = [
        ('itak-gateway', 'FastAPI Gateway', 'http://localhost:8080'),
        ('cloudflared-tunnel', 'Cloudflare Tunnel', 'Check logs for URL'),
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
                install_fastapi_gateway()
                click.pause("  Press any key to continue...")
            elif choice == 2:
                install_cloudflare_temp()
                click.pause("  Press any key to continue...")
            elif choice == 3:
                install_cloudflare_permanent()
                click.pause("  Press any key to continue...")
            elif choice == 4:
                show_service_status()
                click.pause("  Press any key to continue...")
            else:
                print(f"  {YELLOW}Invalid choice. Please enter 0-4.{RESET}")
                
        except click.Abort:
            return
        except Exception as e:
            print(f"  {YELLOW}Error: {e}{RESET}")


if __name__ == '__main__':
    run_api_menu()
