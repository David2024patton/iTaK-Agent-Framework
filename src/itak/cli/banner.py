"""
iTaK CLI Banner - Gemini-Style ASCII Art

Displays the iTaK logo with true-color smooth gradient fades.
"""

from typing import List, Tuple
import sys

# --- THEME DEFINITIONS (Start Hex, End Hex) ---
THEMES = {
    "1. Original Gold":    ("#FFD700", "#FF4500"), # Gold -> OrangeRed
    "2. Neon Cyberpunk":   ("#00FFFF", "#FF00FF"), # Cyan -> Magenta
    "3. Matrix Green":     ("#00FF00", "#003300"), # Lime -> Dark Green
    "4. Inferno":          ("#FFFF00", "#FF0000"), # Yellow -> Red
    "5. Deep Ocean":       ("#00BFFF", "#00008B"), # DeepSkyBlue -> DarkBlue
    "6. Royal Amethyst":   ("#E6E6FA", "#4B0082"), # Lavender -> Indigo
    "7. Miami Sunset":     ("#FF0000", "#FFA500"), # Red -> Orange
    "8. Toxic Sludge":     ("#7FFF00", "#FFFF00"), # Chartreuse -> Yellow
    "9. Glacial Ice":      ("#E0FFFF", "#00FFFF"), # LightCyan -> Cyan
    "10. Noir":            ("#FFFFFF", "#333333"), # White -> Dark Gray
    "11. Electric Violet": ("#8A2BE2", "#FF00FF"), # BlueViolet -> Magenta
    "12. Deep Space":      ("#0000FF", "#000000"), # Blue -> Black
    "13. Candy Floss":     ("#FF69B4", "#87CEEB"), # HotPink -> SkyBlue
    "14. Forest Glade":    ("#00FA9A", "#006400"), # MediumSpringGreen -> DarkGreen
    "15. Red Alert":       ("#FF0000", "#8B0000"), # Red -> DarkRed
    "16. Sunny Day":       ("#FFFFE0", "#FFD700"), # LightYellow -> Gold
    "17. Midnight Run":    ("#191970", "#9400D3"), # MidnightBlue -> DarkViolet
    "18. Hacker Terminal": ("#39FF14", "#0D0D0D"), # NeonGreen -> Near Black
    "19. Retro Wave":      ("#FFD700", "#FF00FF"), # Gold -> Magenta
    "20. Crimson Tide":    ("#FFC0CB", "#DC143C"), # Pink -> Crimson
    "21. Mint Chip":       ("#98FB98", "#2E8B57"), # PaleGreen -> SeaGreen
    "22. Ocean Breeze":    ("#AFEEEE", "#4682B4"), # PaleTurquoise -> SteelBlue
    "23. Golden Hour":     ("#FFA07A", "#8B4513"), # LightSalmon -> SaddleBrown
    "24. Silver Linings":  ("#FFFFFF", "#708090"), # White -> SlateGray
    "25. Bronze Age":      ("#CD7F32", "#8B4500"), # Bronze -> DarkOrange
    "26. Berry Blast":     ("#D8BFD8", "#800080"), # Thistle -> Purple
    "27. Citrus Punch":    ("#FFFF00", "#FF8C00"), # Yellow -> DarkOrange
    "28. Lavender Haze":   ("#E6E6FA", "#9370DB"), # Lavender -> MediumPurple
    "29. Aurora":          ("#00FF7F", "#00BFFF"), # SpringGreen -> DeepSkyBlue
    "30. Steel Blue":      ("#B0C4DE", "#4682B4"), # LightSteelBlue -> SteelBlue
}

# DEFAULT THEME
CURRENT_THEME = "7. Miami Sunset"

# --- CONSTANTS ---
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"

# --- LOGOS ---
ITAK_LOGO_LARGE = [
    "██╗████████╗ █████╗ ██╗  ██╗",
    "██║╚══██╔══╝██╔══██╗██║ ██╔╝",
    "██║   ██║   ███████║█████╔╝ ",
    "██║   ██║   ██╔══██║██╔═██╗ ",
    "██║   ██║   ██║  ██║██║  ██╗",
    "╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝",
]

ITAK_LOGO_BLOCK = [
    "██ ████████  ███████  ██   ██",
    "██    ██    ██    ██  ██  ██ ",
    "██    ██    ████████  █████  ",
    "██    ██    ██    ██  ██  ██ ",
    "██    ██    ██    ██  ██   ██",
]

ITAK_LOGO = [
    "▀█▀ ▀█▀ █▀█ █▄▀",
    " █   █  █▀█ █ █",
]


# --- RGB LOGIC ---

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex string (#RRGGBB) to (r, g, b) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(start_rgb: Tuple[int, int, int], end_rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Linear interpolation between two RGB colors."""
    return tuple(int(start + (end - start) * factor) for start, end in zip(start_rgb, end_rgb))

def generate_gradient_colors(start_hex: str, end_hex: str, steps: int) -> List[str]:
    """Generate a list of ANSI TrueColor escape codes for a smooth gradient."""
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    
    colors = []
    for i in range(steps):
        # Calculate interpolation factor (0.0 to 1.0)
        factor = i / (steps - 1) if steps > 1 else 0.0
        r, g, b = interpolate_color(start_rgb, end_rgb, factor)
        # Create ANSI TrueColor sequence: \033[38;2;R;G;Bm
        colors.append(f"\033[38;2;{r};{g};{b}m")
        
    return colors

# --- RENDER LOGIC ---

# --- RENDER LOGIC ---

def colorize_line(line: str, color_code: str) -> str:
    """Apply specific ANSI color code to a line (Vertical Fade step)."""
    return f"{color_code}{BOLD}{line}{RESET}"

def print_banner(style: str = "large", theme_key: str = None):
    """Print the iTaK banner with vertical smooth gradient."""
    
    # Select Logo
    if style == "block":
        logo = ITAK_LOGO_BLOCK
    elif style == "small":
        logo = ITAK_LOGO
    else:
        logo = ITAK_LOGO_LARGE

    # Select Theme
    theme_key = theme_key or CURRENT_THEME
    if theme_key not in THEMES:
         theme_key = CURRENT_THEME
         
    start_hex, end_hex = THEMES[theme_key]
    
    # Generate Vertical Gradient (Steps = Height)
    height = len(logo)
    colors = generate_gradient_colors(start_hex, end_hex, height)
    
    print()
    for i, line in enumerate(logo):
        # Apply the i-th color to the i-th line
        print(colorize_line(line, colors[i]))
    print()

# --- CLI HELPERS (Keep existing interface) ---
def print_welcome_tips():
    print(f"{DIM}Try these prompts:{RESET}")
    print()
    print(f"  {CYAN}>{RESET} {WHITE}Explain async/await in Python{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}Write a regex for email validation{RESET}")
    print(f"  {CYAN}>{RESET} {WHITE}REST vs GraphQL differences?{RESET}")
    print()

def print_model_info(model: str = "qwen3-vl:4b"):
    print(f"  {DIM}Responding with {CYAN}{model}{RESET}")

def print_status_bar(model: str = "qwen3-vl:4b", mcp_count: int = 0):
    model_info = f"Using: {model}"
    mcp_info = f" | {mcp_count} MCP servers" if mcp_count > 0 else ""
    status_left = f"{DIM}{model_info}{mcp_info}{RESET}"
    status_right = f"{CYAN}local{RESET}"
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except:
        width = 80
    padding = max(10, width - len(model_info) - len(mcp_info) - 10)
    print(f"\n{status_left}{' ' * padding}{status_right}")

def print_prompt():
    print(f"{GREEN}>{RESET} ", end="", flush=True)

def print_response_start(text: str):
    print(f"\n{MAGENTA}✦{RESET} {text}")

def print_awaiting():
    print(f"\n{MAGENTA}✦{RESET} Awaiting your next command or request.\n")

def print_file_operation(operation: str, filename: str):
    print(f"\n  {GREEN}✓{RESET} {BOLD}{operation}{RESET} {DIM}{filename}{RESET}")

def print_code_block(code: str, language: str = "python", filename: str = None):
    if filename:
        print(f"\n  {GREEN}✓{RESET} {BOLD}Writing{RESET} {filename}")
    print(f"  {DIM}┌{'─' * 60}┐{RESET}")
    lines = code.split('\n')
    for i, line in enumerate(lines[:10], 1):
        line_num = f"{i:3}"
        print(f"  {DIM}│{RESET} {CYAN}{line_num}{RESET} {line[:56]}")
    if len(lines) > 10:
        print(f"  {DIM}│ ... ({len(lines) - 10} more lines){RESET}")
    print(f"  {DIM}└{'─' * 60}┘{RESET}")


# --- MAIN (GALLERY) ---
if __name__ == "__main__":
    print(f"\n{BOLD}🎨 iTaK TrueColor Gradient Gallery 🎨{RESET}\n")
    
    for name in THEMES:
        print(f"\n{WHITE}--- {name} ---{RESET}")
        print_banner("large", theme_key=name)
        
    print(f"\n{DIM}To change the default, edit 'CURRENT_THEME' in src/itak/cli/banner.py{RESET}\n")
