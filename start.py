"""iTaK System Health Check & Startup Script

This script performs comprehensive system validation following the iTaK bootstrap protocol.
It scans hardware, verifies Docker services, tests telemetry, and generates a health report.
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

# ANSI Colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

# Phase 1: System Hardware Scan
def scan_system_hardware():
    print_header("PHASE 1: SYSTEM HARDWARE SCAN")
    
    results = {}
    
    # Check WSL vs Windows
    if platform.system() == "Linux" and "microsoft" in platform.uname().release.lower():
        print_success("Running inside WSL (Preferred)")
        results['environment'] = 'WSL'
    elif platform.system() == "Windows":
        print_warning("Running on native Windows (WSL recommended)")
        results['environment'] = 'Windows'
    else:
        print_info(f"Running on {platform.system()}")
        results['environment'] = platform.system()
    
    # Check GPU
    try:
        subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("NVIDIA GPU Detected (CUDA available)")
        results['gpu'] = 'NVIDIA'
    except:
        print_warning("No NVIDIA GPU detected (CPU-only mode)")
        results['gpu'] = 'None'
    
    # CPU and RAM
    cpu_cores = psutil.cpu_count(logical=True)
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    print_success(f"CPU: {cpu_cores} cores")
    print_success(f"RAM: {ram_gb} GB")
    results['cpu_cores'] = cpu_cores
    results['ram_gb'] = ram_gb
    
    # Storage
    print_info("Scanning storage...")
    storage = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            storage.append({
                'mount': part.mountpoint,
                'total_gb': round(usage.total / (1024**3), 1),
                'free_gb': round(usage.free / (1024**3), 1),
                'percent_used': usage.percent
            })
            print(f"   {part.mountpoint}: {round(usage.free / (1024**3), 1)}GB free / {round(usage.total / (1024**3), 1)}GB total")
        except:
            pass
    results['storage'] = storage
    
    # Python version
    py_version = sys.version.split()[0]
    print_success(f"Python: {py_version}")
    results['python_version'] = py_version
    
    return results

# Phase 2: Docker Infrastructure Tests
def test_docker_services():
    print_header("PHASE 2: DOCKER INFRASTRUCTURE")
    
    results = {}
    
    # Check if Docker is running
    try:
        subprocess.run(["docker", "ps"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("Docker is running")
        results['docker'] = 'running'
    except:
        print_error("Docker is not running")
        results['docker'] = 'stopped'
        return results
    
    # Check Ollama (port 11434)
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434", timeout=2) as response:
            if response.status == 200:
                print_success("Ollama API responding (port 11434)")
                results['ollama'] = 'running'
            else:
                print_warning("Ollama API not responding")
                results['ollama'] = 'unhealthy'
    except:
        print_warning("Ollama container not found (port 11434)")
        results['ollama'] = 'stopped'
    
    # Check ChromaDB (port 8900)
    try:
        with urllib.request.urlopen("http://localhost:8900/api/v1/version", timeout=2) as response:
            if response.status == 200:
                print_success("ChromaDB responding (port 8900)")
                results['chromadb'] = 'running'
            else:
                print_warning("ChromaDB not responding")
                results['chromadb'] = 'unhealthy'
    except:
        print_warning("ChromaDB container not found (port 8900)")
        results['chromadb'] = 'stopped'
    
    # Check Context7 (port 29700)
    try:
        with urllib.request.urlopen("http://localhost:29700", timeout=2) as response:
            print_success("Context7 responding (port 29700)")
            results['context7'] = 'running'
    except:
        print_warning("Context7 container not found (port 29700)")
        results['context7'] = 'stopped'
    
    return results

# Phase 3: Telemetry Integration Tests
def test_telemetry():
    print_header("PHASE 3: TELEMETRY INTEGRATION")
    
    results = {}
    
    # Test VPS OTLP collector
    print_info("Testing VPS telemetry stack...")
    try:
        import requests
        import random
        
        tid = ''.join([hex(random.randint(0,15))[2:] for _ in range(32)])
        sid = ''.join([hex(random.randint(0,15))[2:] for _ in range(16)])
        
        data = {
            'resourceSpans': [{
                'resource': {'attributes': [{'key': 'service.name', 'value': {'stringValue': 'itak-health-check'}}]},
                'scopeSpans': [{
                    'spans': [{
                        'traceId': tid,
                        'spanId': sid,
                        'name': 'System Health Check',
                        'kind': 1,
                        'startTimeUnixNano': str(int(time.time()*1e9)),
                        'endTimeUnixNano': str(int((time.time()+1)*1e9)),
                        'attributes': [
                            {'key': 'test.type', 'value': {'stringValue': 'health-check'}},
                            {'key': 'timestamp', 'value': {'stringValue': datetime.now().isoformat()}}
                        ]
                    }]
                }]
            }]
        }
        
        r = requests.post('http://145.79.2.67:4318/v1/traces', json=data, timeout=5)
        if r.status_code == 200:
            print_success(f"VPS Telemetry responding (Trace ID: {tid[:16]}...)")
            results['vps_telemetry'] = 'working'
            results['test_trace_id'] = tid
        else:
            print_warning(f"VPS Telemetry returned status {r.status_code}")
            results['vps_telemetry'] = 'unhealthy'
    except Exception as e:
        print_error(f"VPS Telemetry failed: {e}")
        results['vps_telemetry'] = 'failed'
    
    # Check iTaK telemetry configuration
    try:
        config_path = "src/itak/telemetry/constants.py"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
                if "145.79.2.67:4318" in content:
                    print_success("iTaK telemetry configured for VPS")
                    results['itak_config'] = 'correct'
                else:
                    print_warning("iTaK telemetry endpoint mismatch")
                    results['itak_config'] = 'incorrect'
        else:
            print_warning("iTaK telemetry config not found")
            results['itak_config'] = 'missing'
    except Exception as e:
        print_error(f"Config check failed: {e}")
        results['itak_config'] = 'error'
    
    return results

# Phase 4: iTaK Framework Tests
def test_itak_framework():
    print_header("PHASE 4: iTAK FRAMEWORK")
    
    results = {}
    
    # Check if iTaK is installed
    try:
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        if "itak" in result.stdout.lower():
            print_success("iTaK framework installed")
            results['itak_installed'] = True
            
            # Get version
            for line in result.stdout.split('\n'):
                if 'itak' in line.lower():
                    print_info(f"   {line.strip()}")
        else:
            print_warning("iTaK framework not installed")
            results['itak_installed'] = False
    except:
        print_error("Could not check iTaK installation")
        results['itak_installed'] = False
    
    # Check dependencies
    required_deps = ['requests', 'psutil', 'opentelemetry-api', 'aiosqlite']
    missing_deps = []
    
    try:
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        for dep in required_deps:
            if dep not in result.stdout.lower():
                missing_deps.append(dep)
        
        if not missing_deps:
            print_success("All required dependencies installed")
            results['dependencies'] = 'complete'
        else:
            print_warning(f"Missing dependencies: {', '.join(missing_deps)}")
            results['dependencies'] = 'incomplete'
            results['missing_deps'] = missing_deps
    except:
        print_error("Could not check dependencies")
        results['dependencies'] = 'unknown'
    
    return results

# Generate Report
def generate_report(hardware, docker, telemetry, itak):
    print_header("SYSTEM HEALTH REPORT")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'hardware': hardware,
        'docker_services': docker,
        'telemetry': telemetry,
        'itak_framework': itak
    }
    
    # Calculate health score
    total_checks = 0
    passed_checks = 0
    
    # Docker checks
    for service, status in docker.items():
        if service != 'docker':
            total_checks += 1
            if status == 'running':
                passed_checks += 1
    
    # Telemetry checks
    if telemetry.get('vps_telemetry') == 'working':
        passed_checks += 1
    total_checks += 1
    
    if telemetry.get('itak_config') == 'correct':
        passed_checks += 1
    total_checks += 1
    
    # iTaK checks
    if itak.get('itak_installed'):
        passed_checks += 1
    total_checks += 1
    
    if itak.get('dependencies') == 'complete':
        passed_checks += 1
    total_checks += 1
    
    health_score = round((passed_checks / total_checks) * 100)
    report['health_score'] = health_score
    
    # Print summary
    print(f"\n{Colors.BOLD}Health Score: {health_score}% ({passed_checks}/{total_checks} checks passed){Colors.ENDC}\n")
    
    if health_score >= 80:
        print_success("System is healthy and ready for operation")
    elif health_score >= 60:
        print_warning("System is partially operational - some services need attention")
    else:
        print_error("System needs attention - multiple services are down")
    
    # Save report
    report_path = "system_health_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{Colors.OKBLUE}📊 Full report saved to: {report_path}{Colors.ENDC}")
    
    # Print next steps
    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    if telemetry.get('test_trace_id'):
        print(f"  • View test trace in Grafana: http://145.79.2.67:3456/")
        print(f"    Trace ID: {telemetry['test_trace_id']}")
    if docker.get('ollama') != 'running':
        print(f"  • Start Ollama: docker run -d --gpus=all -p 11434:11434 --name ollama ollama/ollama")
    if docker.get('chromadb') != 'running':
        print(f"  • Start ChromaDB: docker run -d -p 8900:8000 --name shared-chromadb chromadb/chroma")
    
    return report

def main():
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║           iTaK AGENT FRAMEWORK - SYSTEM HEALTH CHECK             ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    print_info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all phases
        hardware = scan_system_hardware()
        docker = test_docker_services()
        telemetry = test_telemetry()
        itak = test_itak_framework()
        
        # Generate report
        report = generate_report(hardware, docker, telemetry, itak)
        
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ Health check complete!{Colors.ENDC}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Health check interrupted by user{Colors.ENDC}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}❌ Health check failed: {e}{Colors.ENDC}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
