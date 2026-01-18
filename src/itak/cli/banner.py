"""
iTaK CLI Banner - Gemini-Style ASCII Art

Displays the iTaK logo with gradient colors on startup.
"""

from typing import List, Tuple

# Color codes for gradient effect (yellow → orange → red)
GRADIENT_COLORS = [
    "\033[93m",  # Bright Yellow (top)
    "\033[33m",  # Orange/Yellow
    "\033[91m",  # Bright Red
    "\033[31m",  # Red (bottom)
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

# Main pixel-art logo (solid blocks matching reference)
ITAK_LOGO_LARGE = [
    "██ ████████  ▄█████▄  ██   ██",
    "██    ██    ██     ██ ██  ██ ",
    "██    ██    █████████ █████  ",
    "██    ██    ██     ██ ██  ██ ",
    "██    ██    ██     ██ ██   ██",
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


def print_banner(style: str = "large"):
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
    
    # Print logo with gradient
    for i, line in enumerate(logo):
        colored_line = colorize_line(line, i)
        print(colored_line)
    
    print()


def print_welcome_tips():
    """Print getting started tips like Gemini CLI."""
    print(f"{DIM}Just start typing to chat, or try these prompts:{RESET}")
    print()
    print(f"  {CYAN}>{RESET} {WHITE}Build a finance SaaS dashboard with charts{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}Build a corporate website with index, about, FAQs, contact{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}Create a blog platform with SEO and analytics{RESET}")
    print()
    print(f"  {CYAN}>{RESET} {WHITE}/create{RESET} {DIM}start a new project{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}/models{RESET} {DIM}change AI model{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}/help{RESET} {DIM}all commands{RESET}  {WHITE}/exit{RESET} {DIM}quit{RESET}")
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
