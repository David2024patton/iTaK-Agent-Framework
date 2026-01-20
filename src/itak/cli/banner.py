"""
iTaK CLI Banner - Gemini-Style ASCII Art

Displays the iTaK logo with gradient colors on startup.
"""

from typing import List, Tuple

# Color codes for gradient effect (5 steps: Yellow → Orange fade)
GRADIENT_COLORS = [
    "\033[38;5;226m",  # Top: Bright Yellow
    "\033[38;5;220m",  # Gold
    "\033[38;5;214m",  # Orange
    "\033[38;5;208m",  # Dark Orange
    "\033[38;5;202m",  # Bottom: Red-Orange
]

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


def colorize_line(line: str, color_index: int = 0) -> str:
    """Apply gradient color to a line."""
    color = GRADIENT_COLORS[color_index % len(GRADIENT_COLORS)]
    return f"{color}{BOLD}{line}{RESET}"



def animate_logo(logo: List[str], duration: float = 1.0):
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
                colored_line = colorize_line(line, color_idx)
                sys.stdout.write(f"{colored_line}\n")
            
            sys.stdout.flush()
            time.sleep(0.1)
            
    finally:
        # Show cursor again
        sys.stdout.write("\033[?25h")


def print_banner(style: str = "large", animate: bool = True, duration: float = 3.0):
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
            animate_logo(logo, duration=duration)
        else:
             # Fallback for non-interactive
            for i, line in enumerate(logo):
                colored_line = colorize_line(line, i)
                print(colored_line)
    else:
        # Static print
        for i, line in enumerate(logo):
            colored_line = colorize_line(line, i)
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
    print_banner("large")
    print_welcome_tips()
    print_prompt()
