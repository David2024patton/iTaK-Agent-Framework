# iTaK Studio Launcher
# Launches CrewAI Studio GUI with iTaK integration

import subprocess
import sys
import os
import click
from pathlib import Path

def get_studio_path():
    """Get the path to the CrewAI Studio app"""
    # Studio is in src/itak/studio/
    studio_dir = Path(__file__).parent.parent / "studio"
    app_path = studio_dir / "app" / "app.py"
    
    if not app_path.exists():
        # Try alternate locations
        alt_paths = [
            studio_dir / "app.py",
            studio_dir / "main.py",
        ]
        for alt in alt_paths:
            if alt.exists():
                return alt
        return None
    
    return app_path

def check_streamlit_installed():
    """Check if streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Install streamlit if not present"""
    click.secho("Installing Streamlit...", fg="yellow")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], 
                   capture_output=True)

def launch_studio(port=8501, no_browser=False):
    """Launch the CrewAI Studio GUI"""
    
    # Check for streamlit
    if not check_streamlit_installed():
        install_streamlit()
    
    # Get studio path
    studio_path = get_studio_path()
    
    if not studio_path:
        click.secho("Error: CrewAI Studio not found!", fg="red")
        click.secho("Run: git submodule update --init --recursive", fg="yellow")
        return False
    
    # Build streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(studio_path),
        "--server.port", str(port),
        "--theme.primaryColor", "#FF6B35",  # iTaK orange
        "--theme.backgroundColor", "#0E1117",
        "--theme.secondaryBackgroundColor", "#262730",
        "--browser.gatherUsageStats", "false",
    ]
    
    if no_browser:
        cmd.extend(["--server.headless", "true"])
    
    # Set working directory to studio folder
    studio_dir = studio_path.parent
    if studio_dir.name == "app":
        studio_dir = studio_dir.parent
    
    # Display launch info
    click.secho("\n" + "="*60, fg="cyan")
    click.secho("  iTaK Studio - Visual Agent Builder", fg="cyan", bold=True)
    click.secho("="*60, fg="cyan")
    click.secho(f"  URL: http://localhost:{port}", fg="green")
    click.secho("  Press Ctrl+C to stop", fg="white", dim=True)
    click.secho("="*60 + "\n", fg="cyan")
    
    # Copy iTaK env vars to studio
    env = os.environ.copy()
    
    # Ensure OLLAMA settings are passed
    if "OLLAMA_HOST" not in env:
        env["OLLAMA_HOST"] = "http://localhost:11434"
    
    # Launch streamlit
    try:
        process = subprocess.Popen(
            cmd,
            cwd=str(studio_dir),
            env=env,
        )
        process.wait()
    except KeyboardInterrupt:
        click.secho("\nShutting down iTaK Studio...", fg="yellow")
        process.terminate()
    
    return True
