"""
iTaK CLI Banner - Gemini-Style ASCII Art

Displays the iTaK logo with gradient colors on startup.
"""

from typing import List, Tuple

# Color codes for gradient effect (5 steps: Yellow → Orange fade)

# 10 Different Color Themes for the User to choose from
THEMES = {
    "1. Original Gold": [
        "\033[38;5;226m", "\033[38;5;220m", "\033[38;5;214m", "\033[38;5;208m", "\033[38;5;202m"
    ],
    "2. Neon Cyberpunk": [
        "\033[38;5;51m", "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;99m", "\033[38;5;129m", "\033[38;5;201m"
    ],
    "3. Matrix Green": [
        "\033[38;5;46m", "\033[38;5;40m", "\033[38;5;34m", "\033[38;5;28m", "\033[38;5;22m"
    ],
    "4. Inferno (Fire)": [
        "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m", "\033[38;5;226m"
    ],
    "5. Deep Ocean": [
        "\033[38;5;27m", "\033[38;5;33m", "\033[38;5;39m", "\033[38;5;45m", "\033[38;5;51m"
    ],
    "6. Royal Amethyst": [
        "\033[38;5;93m", "\033[38;5;99m", "\033[38;5;105m", "\033[38;5;111m", "\033[38;5;117m"
    ],
    "7. Miami Sunset": [
        "\033[38;5;199m", "\033[38;5;205m", "\033[38;5;211m", "\033[38;5;217m", "\033[38;5;223m"
    ],
    "8. Toxic Sludge": [
        "\033[38;5;118m", "\033[38;5;154m", "\033[38;5;190m", "\033[38;5;226m", "\033[38;5;220m"
    ],
    "9. Glacial Ice": [
        "\033[38;5;231m", "\033[38;5;195m", "\033[38;5;159m", "\033[38;5;123m", "\033[38;5;87m"
    ],
    "10. Noir (Monochrome)": [
        "\033[38;5;231m", "\033[38;5;250m", "\033[38;5;244m", "\033[38;5;238m", "\033[38;5;232m"
    ],
    "11. Electric Violet": [
        "\033[38;5;147m", "\033[38;5;141m", "\033[38;5;135m", "\033[38;5;129m", "\033[38;5;123m"
    ],
    "12. Deep Space": [
        "\033[38;5;51m", "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;33m", "\033[38;5;27m"
    ],
    "13. Candy Floss": [
        "\033[38;5;225m", "\033[38;5;219m", "\033[38;5;213m", "\033[38;5;207m", "\033[38;5;201m"
    ],
    "14. Forest Glade": [
        "\033[38;5;154m", "\033[38;5;118m", "\033[38;5;82m", "\033[38;5;46m", "\033[38;5;40m"
    ],
    "15. Red Alert": [
        "\033[38;5;196m", "\033[38;5;160m", "\033[38;5;124m", "\033[38;5;88m", "\033[38;5;52m"
    ],
    "16. Sunny Day": [
        "\033[38;5;229m", "\033[38;5;228m", "\033[38;5;227m", "\033[38;5;226m", "\033[38;5;220m"
    ],
    "17. Midnight Run": [
        "\033[38;5;63m", "\033[38;5;57m", "\033[38;5;56m", "\033[38;5;55m", "\033[38;5;54m"
    ],
    "18. Hacker Terminal": [
        "\033[38;5;120m", "\033[38;5;119m", "\033[38;5;118m", "\033[38;5;46m", "\033[38;5;28m"
    ],
    "19. Retro Wave": [
        "\033[38;5;226m", "\033[38;5;220m", "\033[38;5;214m", "\033[38;5;208m", "\033[38;5;202m"
    ],
    "20. Crimson Tide": [
        "\033[38;5;210m", "\033[38;5;203m", "\033[38;5;196m", "\033[38;5;160m", "\033[38;5;124m"
    ],
    "21. Mint Chip": [
        "\033[38;5;158m", "\033[38;5;151m", "\033[38;5;121m", "\033[38;5;85m", "\033[38;5;49m"
    ],
    "22. Ocean Breeze": [
        "\033[38;5;159m", "\033[38;5;123m", "\033[38;5;87m", "\033[38;5;51m", "\033[38;5;45m"
    ],
    "23. Golden Hour": [
        "\033[38;5;223m", "\033[38;5;222m", "\033[38;5;221m", "\033[38;5;220m", "\033[38;5;214m"
    ],
    "24. Silver Linings": [
        "\033[38;5;255m", "\033[38;5;252m", "\033[38;5;249m", "\033[38;5;246m", "\033[38;5;243m"
    ],
    "25. Bronze Age": [
        "\033[38;5;223m", "\033[38;5;216m", "\033[38;5;180m", "\033[38;5;173m", "\033[38;5;166m"
    ],
    "26. Berry Blast": [
        "\033[38;5;183m", "\033[38;5;177m", "\033[38;5;171m", "\033[38;5;165m", "\033[38;5;129m"
    ],
    "27. Citrus Punch": [
        "\033[38;5;228m", "\033[38;5;227m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;154m"
    ],
    "28. Lavender Haze": [
        "\033[38;5;225m", "\033[38;5;219m", "\033[38;5;189m", "\033[38;5;147m", "\033[38;5;105m"
    ],
    "29. Aurora Borealis": [
        "\033[38;5;51m", "\033[38;5;50m", "\033[38;5;49m", "\033[38;5;48m", "\033[38;5;47m"
    ],
    "30. Steel Blue": [
        "\033[38;5;195m", "\033[38;5;153m", "\033[38;5;111m", "\033[38;5;69m", "\033[38;5;33m"
    ],
}

# START WITH A DEFAULT (Change this string to select a different theme)
CURRENT_THEME = "2. Neon Cyberpunk"
GRADIENT_COLORS = THEMES[CURRENT_THEME]

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"

# iTaK ASCII Art Logo (small)
ITAK_LOGO = [
    "▀█▀ ▀█▀ █▀█ █▄▀",
    " █   █  █▀█ █ █",
]

# Main pixel-art logo (ANSI Shadow style)
ITAK_LOGO_LARGE = [
    "██╗████████╗ █████╗ ██╗  ██╗",
    "██║╚══██╔══╝██╔══██╗██║ ██╔╝",
    "██║   ██║   ███████║█████╔╝ ",
    "██║   ██║   ██╔══██║██╔═██╗ ",
    "██║   ██║   ██║  ██║██║  ██╗",
    "╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝",
]

# Block style logo
ITAK_LOGO_BLOCK = [
    "██ ████████  ███████  ██   ██",
    "██    ██    ██    ██  ██  ██ ",
    "██    ██    ████████  █████  ",
    "██    ██    ██    ██  ██  ██ ",
    "██    ██    ██    ██  ██   ██",
]


def colorize_line(line: str, color_index: int = 0, colors: List[str] = None) -> str:
    """Apply gradient color to a line."""
    if colors is None:
        colors = GRADIENT_COLORS
    color = colors[color_index % len(colors)]
    return f"{color}{BOLD}{line}{RESET}"


def animate_logo(logo: List[str], duration: float = 1.0, colors: List[str] = None):
    """Animate the logo with a shimmering gradient effect."""
    import time
    import sys
    
    cycles = int(duration / 0.1)
    height = len(logo)
    
    # Hide cursor
    sys.stdout.write("\033[?25l")
    
    try:
        for i in range(cycles):
            # Move cursor up to overwrite previous frame (except for first frame)
            if i > 0:
                sys.stdout.write(f"\033[{height}A")
            
            # Print with shifted gradient
            for line_idx, line in enumerate(logo):
                # Shift color index by frame number to create movement
                color_idx = line_idx + i
                colored_line = colorize_line(line, color_idx, colors)
                sys.stdout.write(f"{colored_line}\n")
            
            sys.stdout.flush()
            time.sleep(0.1)
            
        # Final reset: Ensure we end with the static gradient
        sys.stdout.write(f"\033[{height}A")
        for line_idx, line in enumerate(logo):
            colored_line = colorize_line(line, line_idx, colors) # No offset
            sys.stdout.write(f"{colored_line}\n")
        sys.stdout.flush()
            
    finally:
        # Show cursor again
        sys.stdout.write("\033[?25h")


def print_banner(style: str = "large", animate: bool = False, duration: float = 1.0, colors: List[str] = None):
    """Print the iTaK banner with gradient colors."""
    import sys
    
    # Choose logo style
    if style == "block":
        logo = ITAK_LOGO_BLOCK
    elif style == "large":
        logo = ITAK_LOGO_LARGE
    else:
        logo = ITAK_LOGO
    
    print()
    
    if animate and style == "large":
        # Check if we are in a non-interactive shell (CI/CD)
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            animate_logo(logo, duration=duration, colors=colors)
        else:
             # Fallback for non-interactive
            for i, line in enumerate(logo):
                colored_line = colorize_line(line, i, colors)
                print(colored_line)
    else:
        # Static print
        for i, line in enumerate(logo):
            colored_line = colorize_line(line, i, colors)
            print(colored_line)
    
    print()


def print_welcome_tips():
    """Print getting started tips for Chat mode."""
    print(f"{DIM}Try these prompts:{RESET}")
    print()
    print(f"  {CYAN}>{RESET} {WHITE}Explain async/await in Python{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}Write a regex for email validation{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}REST vs GraphQL differences?{RESET}")
    print()


def print_model_info(model: str = "qwen3-vl:4b"):
    """Print the current model info."""
    print(f"  {DIM}Responding with {CYAN}{model}{RESET}")


def print_status_bar(model: str = "qwen3-vl:4b", mcp_count: int = 0):
    """Print status bar at bottom."""
    model_info = f"Using: {model}"
    mcp_info = f" | {mcp_count} MCP servers" if mcp_count > 0 else ""
    
    status_left = f"{DIM}{model_info}{mcp_info}{RESET}"
    status_right = f"{CYAN}local{RESET}"
    
    # Get terminal width
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except:
        width = 80
    
    padding = width - len(model_info) - len(mcp_info) - 5 - 5
    if padding < 0:
        padding = 10
    
    print(f"\n{status_left}{' ' * padding}{status_right}")


def print_prompt():
    """Print the input prompt."""
    print(f"{GREEN}>{RESET} ", end="", flush=True)


def print_response_start(text: str):
    """Print the start of an AI response."""
    print(f"\n{MAGENTA}✦{RESET} {text}")


def print_awaiting():
    """Print awaiting message."""
    print(f"\n{MAGENTA}✦{RESET} Awaiting your next command or request.\n")


def print_file_operation(operation: str, filename: str):
    """Print a file operation indicator."""
    print(f"\n  {GREEN}✓{RESET} {BOLD}{operation}{RESET} {DIM}{filename}{RESET}")


def print_code_block(code: str, language: str = "python", filename: str = None):
    """Print a styled code block."""
    if filename:
        print(f"\n  {GREEN}✓{RESET} {BOLD}Writing{RESET} {filename}")
    
    # Box drawing characters
    print(f"  {DIM}┌{'─' * 60}┐{RESET}")
    
    lines = code.split('\n')
    for i, line in enumerate(lines[:10], 1):  # Limit to 10 lines
        line_num = f"{i:3}"
        print(f"  {DIM}│{RESET} {CYAN}{line_num}{RESET} {line[:56]}")
    
    if len(lines) > 10:
        print(f"  {DIM}│ ... ({len(lines) - 10} more lines){RESET}")
    
    print(f"  {DIM}└{'─' * 60}┘{RESET}")


# Test the banner
if __name__ == "__main__":
    import sys
    
    # Simple gallery mode
    print("\n🎨 iTaK Banner Theme Gallery 🎨\n")
    
    for name, theme_colors in THEMES.items():
        print(f"\n{BOLD}{WHITE}--- {name} ---{RESET}")
        print_banner("large", colors=theme_colors)
    
    print(f"\n{DIM}To change the default, edit 'CURRENT_THEME' in src/itak/cli/banner.py{RESET}\n")
