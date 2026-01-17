# iTaK First-Run Auto-Setup
# Automatically installs all dependencies when user runs any itak command for the first time

import subprocess
import sys
import os
from pathlib import Path

# Flag file to track if setup has been done
SETUP_MARKER = Path.home() / ".itak" / ".setup_complete"

def is_first_run():
    """Check if this is the first time running iTaK"""
    return not SETUP_MARKER.exists()

def mark_setup_complete():
    """Mark that setup has been completed"""
    SETUP_MARKER.parent.mkdir(parents=True, exist_ok=True)
    SETUP_MARKER.write_text("1")

def check_and_install_package(package_name, import_name=None, quiet=False):
    """Check if a package is installed, install if missing"""
    import_name = import_name or package_name
    try:
        __import__(import_name)
        return True
    except ImportError:
        if not quiet:
            print(f"  Installing {package_name}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", package_name],
                stdout=subprocess.DEVNULL if quiet else None,
                stderr=subprocess.DEVNULL if quiet else None
            )
            return True
        except:
            return False

def auto_setup(force=False):
    """
    Auto-install all iTaK dependencies on first run.
    Called automatically when any itak command is run.
    """
    if not force and not is_first_run():
        return True
    
    print("\n" + "="*60)
    print("  iTaK FIRST-RUN SETUP")
    print("  Installing all dependencies...")
    print("="*60 + "\n")
    
    success = True
    
    # Core dependencies (should already be there from pip install itak)
    core_packages = [
        ("click", "click"),
        ("rich", "rich"),
        ("pyyaml", "yaml"),
        ("requests", "requests"),
        ("httpx", "httpx"),
    ]
    
    # Studio dependencies
    studio_packages = [
        ("streamlit", "streamlit"),
    ]
    
    # CrewAI and tools
    crewai_packages = [
        ("crewai", "crewai"),
        ("crewai-tools", "crewai_tools"),
    ]
    
    # Telemetry
    telemetry_packages = [
        ("opentelemetry-api", "opentelemetry"),
        ("opentelemetry-sdk", "opentelemetry.sdk"),
        ("opentelemetry-exporter-otlp-proto-http", "opentelemetry.exporter.otlp.proto.http"),
    ]
    
    # All packages to check/install
    all_packages = core_packages + studio_packages + crewai_packages + telemetry_packages
    
    installed_count = 0
    already_installed = 0
    
    for package, import_name in all_packages:
        try:
            __import__(import_name)
            already_installed += 1
        except ImportError:
            print(f"  [+] Installing {package}...")
            if check_and_install_package(package, import_name, quiet=True):
                installed_count += 1
            else:
                print(f"  [!] Failed to install {package}")
                success = False
    
    # Check for git submodule (Studio)
    studio_path = Path(__file__).parent.parent / "studio"
    if studio_path.exists() and not (studio_path / "app").exists():
        print("  [+] Initializing Studio submodule...")
        try:
            # Find the repo root
            repo_root = Path(__file__).parent.parent.parent.parent
            subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"],
                cwd=str(repo_root),
                capture_output=True
            )
        except:
            print("  [!] Could not initialize Studio submodule")
    
    # Summary
    print("\n" + "-"*60)
    if installed_count > 0:
        print(f"  Installed {installed_count} new packages")
    print(f"  {already_installed} packages already installed")
    print("-"*60 + "\n")
    
    if success:
        mark_setup_complete()
        print("  [OK] iTaK setup complete! All dependencies installed.\n")
    
    return success

def reset_setup():
    """Reset the setup marker to force re-run on next command"""
    if SETUP_MARKER.exists():
        SETUP_MARKER.unlink()
        return True
    return False
