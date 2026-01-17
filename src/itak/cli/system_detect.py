# System Detection for iTaK Model Selection
# Detects VRAM, RAM, and disk space to filter compatible models

import subprocess
import shutil
import platform
import os

def get_system_specs():
    """
    Detect system specifications for model filtering.
    Returns dict with vram_gb, ram_gb, disk_gb
    """
    specs = {
        "vram_gb": 0,
        "ram_gb": 0,
        "disk_gb": 0,
        "gpu_name": None,
        "os": platform.system(),
    }
    
    # Get RAM
    try:
        if platform.system() == "Windows":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulong = ctypes.c_ulong
            class MEMORYSTATUS(ctypes.Structure):
                _fields_ = [
                    ('dwLength', c_ulong),
                    ('dwMemoryLoad', c_ulong),
                    ('dwTotalPhys', c_ulong),
                    ('dwAvailPhys', c_ulong),
                    ('dwTotalPageFile', c_ulong),
                    ('dwAvailPageFile', c_ulong),
                    ('dwTotalVirtual', c_ulong),
                    ('dwAvailVirtual', c_ulong),
                ]
            memoryStatus = MEMORYSTATUS()
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
            kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
            specs["ram_gb"] = memoryStatus.dwTotalPhys / (1024**3)
        else:
            # Linux/Mac
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if 'MemTotal' in line:
                        specs["ram_gb"] = int(line.split()[1]) / (1024**2)
                        break
    except:
        specs["ram_gb"] = 8  # Default assumption
    
    # Get VRAM (NVIDIA GPU)
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.total,name', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    vram_mb = float(parts[0].strip())
                    specs["vram_gb"] = max(specs["vram_gb"], vram_mb / 1024)
                    specs["gpu_name"] = parts[1].strip()
    except:
        pass
    
    # Get Disk Space
    try:
        total, used, free = shutil.disk_usage("/")
        specs["disk_gb"] = free / (1024**3)
    except:
        try:
            # Windows fallback
            total, used, free = shutil.disk_usage("C:\\")
            specs["disk_gb"] = free / (1024**3)
        except:
            specs["disk_gb"] = 50  # Default assumption
    
    return specs

def parse_size_to_gb(size_str):
    """Convert size string like '4.7GB' or '986MB' to GB float"""
    size_str = size_str.upper().strip()
    try:
        if 'GB' in size_str:
            return float(size_str.replace('GB', ''))
        elif 'MB' in size_str:
            return float(size_str.replace('MB', '')) / 1024
        else:
            return float(size_str)
    except:
        return 0

def get_required_vram(model_size_gb):
    """
    Estimate VRAM needed to run a model.
    Rule of thumb: model size + ~2GB overhead for inference
    """
    return model_size_gb + 2.0

def can_run_on_gpu(model_size_gb, vram_gb):
    """Check if model can run on GPU"""
    required = get_required_vram(model_size_gb)
    return vram_gb >= required

def can_run_on_cpu(model_size_gb, ram_gb):
    """Check if model can run on CPU (slower but works)"""
    # CPU needs model size + ~4GB for OS and overhead
    required = model_size_gb + 4.0
    return ram_gb >= required

def can_download(model_size_gb, disk_gb):
    """Check if there's enough disk space to download"""
    # Need model size + some buffer
    required = model_size_gb * 1.2  # 20% buffer
    return disk_gb >= required

def get_model_compatibility(model_info, specs):
    """
    Determine if a model is compatible with the system.
    Returns: 'gpu' (fast), 'cpu' (slow), 'no_disk' (can't download), 'incompatible'
    """
    model_size = parse_size_to_gb(model_info.get('size', '0GB'))
    
    # Check disk space first
    if not can_download(model_size, specs['disk_gb']):
        return 'no_disk'
    
    # Check GPU
    if specs['vram_gb'] > 0 and can_run_on_gpu(model_size, specs['vram_gb']):
        return 'gpu'
    
    # Check CPU fallback
    if can_run_on_cpu(model_size, specs['ram_gb']):
        return 'cpu'
    
    return 'incompatible'

def get_recommendation_tier(specs):
    """
    Based on system specs, recommend a model tier.
    Returns max model size in GB that should run well.
    """
    if specs['vram_gb'] >= 24:
        return 32  # Can run 32B models
    elif specs['vram_gb'] >= 16:
        return 14  # Can run 14B models  
    elif specs['vram_gb'] >= 12:
        return 8   # Can run 8B models well
    elif specs['vram_gb'] >= 8:
        return 7   # Can run 7B models
    elif specs['vram_gb'] >= 6:
        return 4   # Can run 4B models
    elif specs['vram_gb'] >= 4:
        return 3   # Can run 3B models
    else:
        # CPU only - use RAM
        if specs['ram_gb'] >= 32:
            return 8
        elif specs['ram_gb'] >= 16:
            return 4
        else:
            return 1.5

def format_specs_summary(specs):
    """Format system specs as a nice string"""
    parts = []
    
    if specs['gpu_name']:
        parts.append(f"GPU: {specs['gpu_name']} ({specs['vram_gb']:.1f}GB VRAM)")
    elif specs['vram_gb'] > 0:
        parts.append(f"VRAM: {specs['vram_gb']:.1f}GB")
    else:
        parts.append("GPU: Not detected (CPU mode)")
    
    parts.append(f"RAM: {specs['ram_gb']:.1f}GB")
    parts.append(f"Disk: {specs['disk_gb']:.1f}GB free")
    
    return " | ".join(parts)
