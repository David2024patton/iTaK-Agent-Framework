"""iTaK Framework Bootstrap & Auto-Deployment Script

This script is executed during iTaK's first-time setup. It:
1. Scans system hardware
2. Auto-deploys all necessary Docker containers
3. Configures telemetry to point to VPS
4. Sets up the complete iTaK environment

Based on the iTaK Bootstrap Protocol from this.md
"""

import platform
import subprocess
import sys
import time
import os
import json
import psutil
import urllib.request
from datetime import datetime
from pathlib import Path

# ANSI Colors
class C:
    H = '\033[95m\033[1m'  # Header
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    R = '\033[91m'  # Red
    B = '\033[94m'  # Blue
    E = '\033[0m'   # End

def print_header(text):
    print(f"\n{C.H}{'='*70}\n{text.center(70)}\n{'='*70}{C.E}\n")

def print_success(text):
    print(f"{C.G}✅ {text}{C.E}")

def print_warning(text):
    print(f"{C.Y}⚠️  {text}{C.E}")

def print_error(text):
    print(f"{C.R}❌ {text}{C.E}")

def print_info(text):
    print(f"{C.B}ℹ️  {text}{C.E}")

# Check and install Python dependencies
def check_and_install_dependencies():
    print_header("CHECKING PYTHON DEPENDENCIES")
    
    required_packages = {
        'requests': 'requests',
        'opentelemetry-api': 'opentelemetry',
        'opentelemetry-sdk': 'opentelemetry.sdk',
        'litellm': 'litellm',
        'chromadb': 'chromadb',
        'psutil': 'psutil'
    }
    
    # Check for crewai_tools separately (installed via crewai[tools])
    crewai_tools_installed = False
    try:
        import crewai_tools
        print_success("crewai[tools] installed")
        crewai_tools_installed = True
    except ImportError:
        print_warning("crewai[tools] missing")
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print_success(f"{package_name} installed")
        except ImportError:
            print_warning(f"{package_name} missing")
            missing_packages.append(package_name)
    
    # Install missing packages
    if missing_packages or not crewai_tools_installed:
        packages_to_install = missing_packages.copy()
        if not crewai_tools_installed:
            packages_to_install.append("'crewai[tools]'")
        
        print_info(f"Installing {len(packages_to_install)} missing packages...")
        try:
            # Install regular packages
            if missing_packages:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--quiet'
                ] + missing_packages)
                print_success(f"Installed: {', '.join(missing_packages)}")
            
            # Install crewai[tools] separately (needs special handling)
            if not crewai_tools_installed:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--quiet', 'crewai[tools]'
                ])
                print_success("Installed: crewai[tools]")
                
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install packages: {e}")
            print_info("Please run manually: pip install " + " ".join(packages_to_install))
    else:
        print_success("All Python dependencies installed")



# Step 1: Identity
def get_user_identity():
    print_header("STEP 1: IDENTITY SETUP")
    name = input(f"{C.B}Before we start, what is your name? {C.E}").strip()
    if not name:
        name = "User"
    print_success(f"Welcome, {name}!")
    return name

# Step 3: Environment Verification (WSL & GPU)
def verify_environment():
    print_header("STEP 3: ENVIRONMENT VERIFICATION")
    
    env_info = {}
    
    # Check WSL vs Windows
    if platform.system() == "Linux" and "microsoft" in platform.uname().release.lower():
        print_success("Running inside WSL (Preferred)")
        env_info['platform'] = 'WSL'
    elif platform.system() == "Windows":
        print_warning("Running on native Windows (WSL recommended for better compatibility)")
        env_info['platform'] = 'Windows'
    else:
        print_info(f"Running on {platform.system()}")
        env_info['platform'] = platform.system()
    
    # Check Docker
    print_info("Checking Docker...")
    try:
        subprocess.run(["docker", "ps"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("Docker is running")
        env_info['docker'] = True
    except:
        print_error("Docker is not running")
        print_info("Attempting to start Docker...")
        try:
            if platform.system() == "Windows":
                subprocess.run(["net", "start", "com.docker.service"], check=True)
            else:
                subprocess.run(["sudo", "service", "docker", "start"], check=True)
            time.sleep(5)
            print_success("Docker started successfully")
            env_info['docker'] = True
        except:
            print_error("Failed to start Docker automatically")
            print_warning("Please start Docker manually and run this script again")
            sys.exit(1)
    
    # Check GPU
    try:
        subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("NVIDIA GPU Detected (CUDA available)")
        env_info['gpu'] = 'NVIDIA'
    except:
        print_warning("No NVIDIA GPU detected (CPU-only mode)")
        env_info['gpu'] = None
    
    # System specs
    cpu_cores = psutil.cpu_count(logical=True)
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    print_success(f"CPU: {cpu_cores} cores")
    print_success(f"RAM: {ram_gb} GB")
    env_info['cpu_cores'] = cpu_cores
    env_info['ram_gb'] = ram_gb
    
    return env_info

# Step 5: Backend Discovery & Active Healing
def setup_backend(env_info):
    print_header("STEP 5: BACKEND AUTO-DEPLOYMENT")
    
    # Check if Ollama is running
    def is_ollama_running():
        try:
            with urllib.request.urlopen("http://127.0.0.1:11434", timeout=2) as response:
                return response.status == 200
        except:
            return False
    
    if is_ollama_running():
        print_success("Ollama is already running")
    else:
        print_info("Ollama not found. Deploying Ollama container...")
        try:
            # Check if container exists but is stopped
            check = subprocess.run(["docker", "ps", "-a", "--filter", "name=ollama", "--format", "{{.Names}}"], 
                                 capture_output=True, text=True)
            if "ollama" in check.stdout:
                print_info("Starting existing Ollama container...")
                subprocess.run(["docker", "start", "ollama"], check=True)
            else:
                # Deploy new container
                cmd = [
                    "docker", "run", "-d",
                    "--gpus=all" if env_info.get('gpu') == 'NVIDIA' else "--rm",
                    "-v", "ollama:/root/.ollama",
                    "-p", "11434:11434",
                    "--name", "ollama",
                    "--restart", "unless-stopped",
                    "ollama/ollama"
                ]
                subprocess.run(cmd, check=True)
            
            print_info("Waiting for Ollama to start...")
            for _ in range(10):
                if is_ollama_running():
                    print_success("Ollama deployed and running")
                    break
                time.sleep(2)
        except Exception as e:
            print_error(f"Failed to deploy Ollama: {e}")
            print_warning("You can deploy it manually later with: docker run -d -p 11434:11434 --name ollama ollama/ollama")
    
    # Check if ChromaDB is running
    def is_chroma_running():
        try:
            with urllib.request.urlopen("http://localhost:29900/api/v1/version", timeout=2) as response:
                return response.status == 200
        except:
            return False
    
    if is_chroma_running():
        print_success("ChromaDB is already running")
    else:
        print_info("ChromaDB not found. Deploying ChromaDB container...")
        try:
            check = subprocess.run(["docker", "ps", "-a", "--filter", "name=shared-chromadb", "--format", "{{.Names}}"],
                                 capture_output=True, text=True)
            if "shared-chromadb" in check.stdout:
                subprocess.run(["docker", "start", "shared-chromadb"], check=True)
            else:
                subprocess.run([
                    "docker", "run", "-d",
                    "--name", "shared-chromadb",
                    "-p", "29900:8000",
                    "--restart", "unless-stopped",
                    "chromadb/chroma"
                ], check=True)
            
            print_info("Waiting for ChromaDB to start...")
            for _ in range(10):
                if is_chroma_running():
                    print_success("ChromaDB deployed and running")
                    break
                time.sleep(2)
        except Exception as e:
            print_error(f"Failed to deploy ChromaDB: {e}")
            print_warning("You can deploy it manually later")

# Configure Telemetry
def configure_telemetry():
    print_header("TELEMETRY CONFIGURATION")
    
    config_path = Path("src/itak/telemetry/constants.py")
    
    if not config_path.exists():
        print_warning("Telemetry config not found - iTaK may not be installed yet")
        return
    
    # Read current config
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Check if already configured
    if "145.79.2.67:4318" in content:
        print_success("Telemetry already configured for VPS")
    else:
        print_info("Configuring telemetry to send to VPS...")
        # Update the endpoint
        content = content.replace(
            'http://145.79.2.67:4319',
            'http://145.79.2.67:4318'
        )
        with open(config_path, 'w') as f:
            f.write(content)
        print_success("Telemetry configured to send to VPS (145.79.2.67:4318)")

# Generate System Profile
def generate_system_profile(user_name, env_info):
    print_header("GENERATING SYSTEM PROFILE")
    
    # Get storage info
    storage = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            storage.append({
                'mount': part.mountpoint,
                'total_gb': round(usage.total / (1024**3), 1),
                'free_gb': round(usage.free / (1024**3), 1)
            })
        except:
            pass
    
    profile = {
        'user': user_name,
        'timestamp': datetime.now().isoformat(),
        'platform': env_info.get('platform'),
        'gpu': env_info.get('gpu'),
        'cpu_cores': env_info.get('cpu_cores'),
        'ram_gb': env_info.get('ram_gb'),
        'storage': storage,
        'python_version': sys.version.split()[0]
    }
    
    # Save profile
    os.makedirs('users/docs', exist_ok=True)
    with open('users/docs/system_profile.json', 'w') as f:
        json.dump(profile, f, indent=2)
    
    print_success("System profile saved to users/docs/system_profile.json")
    return profile

# Main Bootstrap
def main():
    print(f"\n{C.H}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║         iTaK AGENT FRAMEWORK - BOOTSTRAP & AUTO-DEPLOY           ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{C.E}\n")
    
    try:
        # Step 0: Check and install dependencies
        check_and_install_dependencies()
        
        # Step 1: Identity
        user_name = get_user_identity()
        
        # Step 3: Environment Verification
        env_info = verify_environment()
        
        # Step 4: Dependencies (assume already done via pip install)
        print_header("STEP 4: DEPENDENCIES")
        print_info("Checking dependencies...")
        try:
            import requests
            import opentelemetry
            print_success("Core dependencies installed")
        except ImportError as e:
            print_warning(f"Missing dependency: {e}")
            print_info("Run: pip install -r requirements.txt")
        
        # Step 5: Backend Auto-Deployment
        setup_backend(env_info)
        
        # Configure Telemetry
        configure_telemetry()
        
        # Generate System Profile
        profile = generate_system_profile(user_name, env_info)
        
        # Final Summary
        print_header("✅ BOOTSTRAP COMPLETE")
        print(f"{C.G}")
        print(f"System Online, {user_name}!")
        print(f"Platform: {env_info.get('platform')}")
        print(f"GPU: {env_info.get('gpu') or 'CPU-only'}")
        print(f"Resources: {env_info.get('cpu_cores')} cores, {env_info.get('ram_gb')}GB RAM")
        print(f"\nServices Deployed:")
        print(f"  • Ollama (LLM Backend): http://localhost:11434")
        print(f"  • ChromaDB (Memory): http://localhost:29900")
        print(f"  • VPS Telemetry: http://145.79.2.67:4318")
        print(f"\nNext Steps:")
        print(f"  1. Run: python -m itak.cli to start using iTaK")
        print(f"  2. View telemetry in Grafana: http://145.79.2.67:3456")
        print(f"{C.E}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}⚠️  Bootstrap interrupted by user{C.E}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{C.R}❌ Bootstrap failed: {e}{C.E}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
