"""
iTaK Optional Services Manager
Install and manage optional heavy services (Supabase, ComfyUI, Whisper, Redis)
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
RED = "\033[31m"

# Project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DOCKER_DIR = PROJECT_ROOT / 'docker' / 'api-gateway'
ENV_FILE = PROJECT_ROOT / '.env'

# Optional services configuration
OPTIONAL_SERVICES = {
    'redis': {
        'name': 'Redis',
        'desc': 'Caching, Queues, Session Storage',
        'container': 'redis',
        'port': 63790,
        'env_var': 'REDIS_URL',
        'url': 'redis://localhost:63790',
        'needs_credentials': False,
        'needs_gpu': False,
    },
    'whisper': {
        'name': 'Whisper',
        'desc': 'Speech-to-Text (GPU accelerated)',
        'container': 'whisper',
        'port': 59247,
        'env_var': 'WHISPER_URL',
        'url': 'http://localhost:59247',
        'needs_credentials': False,
        'needs_gpu': True,
    },
    'comfyui': {
        'name': 'ComfyUI',
        'desc': 'AI Image Generation (GPU required)',
        'container': 'comfyui',
        'port': 58127,
        'env_var': 'COMFYUI_URL',
        'url': 'http://localhost:58127',
        'needs_credentials': False,
        'needs_gpu': True,
    },
    'supabase': {
        'name': 'Supabase',
        'desc': 'PostgreSQL + Studio Dashboard',
        'container': 'supabase-db',
        'port': 54321,
        'env_var': 'SUPABASE_URL',
        'url': 'postgresql://localhost:54321',
        'needs_credentials': True,
        'needs_gpu': False,
        'extra_containers': ['supabase-studio'],
    },
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_container_status(name):
    """Get status of a Docker container."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f'name=^{name}$', '--format', '{{.Status}}'],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        if 'Up' in status:
            return 'running'
        elif status:
            return 'stopped'
        return 'not_installed'
    except:
        return 'error'


def check_nvidia_gpu():
    """Check if NVIDIA GPU is available."""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def update_env_file(key, value):
    """Add or update a key in the .env file."""
    env_content = ''
    key_found = False
    
    if ENV_FILE.exists():
        env_content = ENV_FILE.read_text()
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith(f'{key}=') or line.startswith(f'# {key}='):
                new_lines.append(f'{key}={value}')
                key_found = True
            else:
                new_lines.append(line)
        env_content = '\n'.join(new_lines)
    
    if not key_found:
        env_content += f'\n{key}={value}\n'
    
    ENV_FILE.write_text(env_content)


def start_service(service_key):
    """Start an optional service using docker compose with profile."""
    service = OPTIONAL_SERVICES[service_key]
    
    print(f"\n  {CYAN}🚀 Installing {service['name']}...{RESET}")
    print(f"  {DIM}This may take a few minutes for first-time setup{RESET}")
    print()
    
    try:
        compose_file = DOCKER_DIR / 'docker-compose.yml'
        
        # Check if image needs to be pulled
        print(f"  {DIM}[1/3] Pulling Docker image...{RESET}", flush=True)
        
        result = subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), '-p', 'api-gateway',
             '--profile', 'optional', 'up', '-d', service['container']],
            capture_output=True, text=True, cwd=str(DOCKER_DIR)
        )
        
        print(f"  {DIM}[2/3] Starting container...{RESET}", flush=True)
        
        # Also start extra containers if any
        if 'extra_containers' in service:
            for extra in service['extra_containers']:
                print(f"  {DIM}[2/3] Starting {extra}...{RESET}", flush=True)
                subprocess.run(
                    ['docker', 'compose', '-f', str(compose_file), '-p', 'api-gateway',
                     '--profile', 'optional', 'up', '-d', extra],
                    capture_output=True, text=True, cwd=str(DOCKER_DIR)
                )
        
        print(f"  {DIM}[3/3] Configuring...{RESET}", flush=True)
        
        if result.returncode == 0:
            # Update .env file
            update_env_file(service['env_var'], service['url'])
            print(f"\n  {GREEN}✅ {service['name']} installed and started!{RESET}")
            print(f"     {DIM}{service['url']}{RESET}")
            return True
        else:
            print(f"\n  {RED}❌ Failed to start {service['name']}{RESET}")
            if result.stderr:
                print(f"     {DIM}{result.stderr[:200]}{RESET}")
            return False
    except Exception as e:
        print(f"\n  {RED}❌ Error: {e}{RESET}")
        return False


def stop_service(service_key):
    """Stop an optional service."""
    service = OPTIONAL_SERVICES[service_key]
    
    print(f"\n  {DIM}Stopping {service['name']}...{RESET}")
    
    try:
        subprocess.run(['docker', 'stop', service['container']], capture_output=True)
        
        if 'extra_containers' in service:
            for extra in service['extra_containers']:
                subprocess.run(['docker', 'stop', extra], capture_output=True)
        
        print(f"  {YELLOW}⏸️  {service['name']} stopped{RESET}")
        return True
    except Exception as e:
        print(f"  {RED}❌ Error: {e}{RESET}")
        return False


def install_with_credentials(service_key):
    """Install a service that requires credentials (Supabase)."""
    import click
    
    service = OPTIONAL_SERVICES[service_key]
    
    print(f"\n  {CYAN}🔧 Configure {service['name']}{RESET}\n")
    
    if service_key == 'supabase':
        print(f"  {DIM}Enter database credentials (or press Enter for defaults):{RESET}\n")
        
        username = click.prompt('  PostgreSQL Username', default='postgres')
        password = click.prompt('  PostgreSQL Password', default='postgres', hide_input=False)
        database = click.prompt('  Database Name', default='postgres')
        
        # Update docker-compose environment variables dynamically
        # For now, we'll use the defaults but save to .env
        update_env_file('POSTGRES_USER', username)
        update_env_file('POSTGRES_PASSWORD', password)
        update_env_file('POSTGRES_DB', database)
        
        print(f"\n  {DIM}Credentials saved to .env{RESET}")
        
        # Start the service
        return start_service(service_key)
    
    return False


def print_optional_menu():
    """Print the optional services menu."""
    clear_screen()
    
    print(f"\n  \033[35m╔══════════════════════════════════════════════════════════════╗\033[0m")
    print(f"  \033[35m║  🧩 Optional Services                                        ║\033[0m")
    print(f"  \033[35m╚══════════════════════════════════════════════════════════════╝\033[0m")
    print()
    
    print(f"  \033[90m┌───────────────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[90m│  💡 Heavy services installed on-demand                        │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m│    🗄️ Redis    → Caching, queues, sessions                   │\033[0m")
    print(f"  \033[90m│    🎙️ Whisper  → Speech-to-text (GPU)                         │\033[0m")
    print(f"  \033[90m│    🎨 ComfyUI  → AI image generation (GPU)                    │\033[0m")
    print(f"  \033[90m│    🐘 Supabase → PostgreSQL + Studio                          │\033[0m")
    print(f"  \033[90m│                                                               │\033[0m")
    print(f"  \033[90m└───────────────────────────────────────────────────────────────┘\033[0m")
    print()
    
    has_gpu = check_nvidia_gpu()
    
    idx = 1
    for key, service in OPTIONAL_SERVICES.items():
        status = get_container_status(service['container'])
        
        # Status indicator
        if status == 'running':
            status_str = f"{GREEN}Running{RESET}"
            action = "Stop"
        elif status == 'stopped':
            status_str = f"{YELLOW}Stopped{RESET}"
            action = "Start"
        else:
            status_str = f"{DIM}Not installed{RESET}"
            action = "Install"
        
        # GPU warning
        gpu_warn = ""
        if service['needs_gpu'] and not has_gpu:
            gpu_warn = f" {YELLOW}(GPU required){RESET}"
        
        print(f"  [{idx}] {service['name']}: {status_str}{gpu_warn}")
        print(f"      {DIM}{service['desc']}{RESET}")
        idx += 1
    
    print(f"\n  [0] ← Back to Main Menu\n")


def run_optional_services_menu():
    """Run the optional services submenu."""
    while True:
        print_optional_menu()
        
        try:
            choice = input(f"  Choice [0]: ").strip()
            
            if not choice or choice == '0':
                return
            
            choice_num = int(choice)
            services_list = list(OPTIONAL_SERVICES.keys())
            
            if 1 <= choice_num <= len(services_list):
                service_key = services_list[choice_num - 1]
                service = OPTIONAL_SERVICES[service_key]
                status = get_container_status(service['container'])
                
                if status == 'running':
                    stop_service(service_key)
                elif service['needs_credentials'] and status == 'not_installed':
                    install_with_credentials(service_key)
                else:
                    # Check GPU requirement
                    if service['needs_gpu'] and not check_nvidia_gpu():
                        print(f"\n  {YELLOW}⚠️  Warning: {service['name']} requires an NVIDIA GPU{RESET}")
                        confirm = input(f"  {DIM}Try anyway? (y/N): {RESET}").strip().lower()
                        if confirm != 'y':
                            input("\n  Press any key to continue...")
                            continue
                    
                    start_service(service_key)
                
                input("\n  Press any key to continue...")
            else:
                print(f"  {YELLOW}Invalid choice{RESET}")
                
        except ValueError:
            print(f"  {YELLOW}Invalid input{RESET}")
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    run_optional_services_menu()
