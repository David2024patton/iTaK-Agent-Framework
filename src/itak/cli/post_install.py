"""
iTaK Post-Install Auto-Launch

This module is called as a console script entry point after pip install.
When user runs `pip install itak`, this automatically launches the CLI.
"""

import sys
import subprocess


def post_install_launch():
    """
    Auto-launch iTaK CLI after pip install.
    This is registered as a console_scripts entry point that pip calls after install.
    """
    print("\n" + "="*60)
    print("  iTaK installed successfully!")
    print("  Launching iTaK...")
    print("="*60 + "\n")
    
    # Launch the actual itak CLI
    try:
        # Import and run the CLI directly
        from itak.cli.cli import main
        main()
    except ImportError:
        # Fallback: run as subprocess
        subprocess.run([sys.executable, "-m", "itak.cli.cli"])
    except Exception as e:
        print(f"\n  Note: Run 'itak' to start the iTaK Agent Framework")
        print(f"  Error: {e}\n")


if __name__ == "__main__":
    post_install_launch()
