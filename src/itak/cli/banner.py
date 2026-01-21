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
# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

class Theme:
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"

# --- WIZARD ASCII ART (Compact) ---
WIZARD_ASCII = [
    "        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠀⠀⠀⠀⡰⠉⠀⠀⠉⠻⢦⡀⠀⡀⠀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠀⠀⠀⣰⠁⠀⠀⠀⠀⠈⣶⣝⣺⢷⡀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠀⠀⢠⡗⠂⠀⠀⠀⠁⠐⠺⡌⠁⠈⠛⠂⠀⠀",
    "        ⠀⠀⠀⢀⣠⠴⠚⠊⠉⠉⠁⠈⠉⠉⠑⠓⠦⣄⡀⠀⠀⠀",
    "        ⢀⣴⣾⣭⡤⢤⣤⣄⣀⣀⣀⣀⣀⣀⣠⣤⡤⢤⣭⣷⣦⡀",
    "        ⠈⢯⣿⡿⣁⡜⣨⠀⠷⣲⡞⢻⣖⠾⠀⡅⢳⣈⢿⣟⡽⠁",
    "        ⠀⠀⠈⠙⡟⡜⣸⡀⠀⡅⠇⠘⠢⠀⢀⣇⢣⢻⠋⠁⠀⠀",
    "        ⠀⠀⠀⠰⡾⡰⡏⠛⠚⠋⣉⣍⠙⠓⠛⢹⢆⢷⠆⠀⠀⠀",
    "        ⠀⠀⠀⠀⢷⠡⢹⠒⢖⡬⠄⠀⢭⡲⠒⡏⠈⡾⠀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠸⢇⣏⣦⠀⠀⠀⠀⠀⠀⣴⣽⡼⠇⠀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠀⠈⠈⠉⠻⣴⠀⠀⣤⠟⠁⠁⠁⠀⠀⠀⠀⠀",
    "        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀",
]

# --- LOGOS ---
ITAK_LOGO_LARGE = [
    "██╗████████╗ █████╗ ██╗  ██╗",
    "██║╚══██╔══╝██╔══██╗██║ ██╔╝",
    "██║   ██║   ███████║█████╔╝ ",
    "██║   ██║   ██╔══██║██╔═██╗ ",
    "██║   ██║   ██║  ██║██║  ██╗",
    "╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝",
]

ITAK_LOGO_CYBER = [
    "  ▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄   ▄▄",
    "  ███  ▀▀▀███▀ ▀▀████▄  ███  ▄██",
    "  ███     ███    █████▄ ███ ▄██▀",
    "  ███     ███    ██████▄███▄██▀ ",
    "  ███     ███    ███▀████████▀  ",
    "  ███     ███    ███  ▀█████▀   ",
    "  ███     ███    ███   ▀███▀    ",
]

ITAK_LOGO_MODERN = [
    "   │  ┌┬┐  ┌─┐  ┬┌─",
    "   │   │   ├─┤  ├┴┐",
    "   │   ┴   ┴ ┴  ┴ ┴",
]

ITAK_LOGO_PIXEL = [
    " ▀█▀ ▀█▀ █▀█ █ █ ",
    "  █   █  █▀█ █▀▄ ",
    " ▀▀▀  ▀  ▀ ▀ ▀ ▀ ",
]

# --- SHADOW STYLE ---
ITAK_LOGO_SHADOW = [
    "██╗ ▄▄▄▄▄▄▄▄╗  ▄▄▄▄▄▄▄▄╗ ██╗  ██╗",
    "██║ ╚══██╔══╝ ▄█▀▀▀▀▀▀▀█▄ ██║ ██╔╝",
    "██║    ██║    ██║     ██║ █████╔╝ ",
    "██║    ██║    ██████████║ ██╔═██╗ ",
    "██║    ██║    ██║     ██║ ██║  ██╗",
    "╚═╝    ╚═╝    ╚═╝     ╚═╝ ╚═╝  ╚═╝",
]

# --- 3D DASHED PARTS ---
D3D_ARROW = [
    " / /      ",
    "/ / /     ",
    "\\ \\ \\    ",
    " \\ \\ \\   ",
    "  \\ \\ \\  ",
    "   \\ \\    ",
]

D3D_I = [
    "  __   ",
    " |  |  ",
    " |  |  ",
    " |  |  ",
    " |  |  ",
    " |__|  ",
]

D3D_T = [
    " _______  ",
    "|__   __| ",
    "   | |    ",
    "   | |    ",
    "   | |    ",
    "   |_|    ",
]

D3D_A = [
    "     __      ",
    "    /  \     ",
    "   / /\ \    ",
    "  / /__\ \   ",
    " /  ____  \  ",
    "/__/    \__\ ",
]

D3D_K = [
    "  __   __ ",
    " |  | / / ",
    " |  |/ /  ",
    " |     \  ",
    " |  |\  \ ",
    " |__| \__\\",
]

def join_art(*parts):
    """Combine ASCII art columns horizontally."""
    return ["".join(lines) for lines in zip(*parts)]

ITAK_LOGO_DASH_3D = join_art(D3D_ARROW, D3D_I, D3D_T, D3D_A, D3D_K)

ITAK_LOGO_3D = [
    "  _____ _______    _      _  __",
    " |_   _|__   __|  / \    | |/ /",
    "   | |    | |    / _ \   | ' / ",
    "   | |    | |   / ___ \  | . \ ",
    "  _| |_   | |  / /   \ \ | |\ \ ",
    " |_____|  |_| /_/     \_\|_| \_\\",
]

ITAK_LOGO_SLANT = [
    "    ____  ______   ___     __ __",
    "   /  _/ /_  __/  /   |   / //_/",
    "   / /    / /    / /| |  / ,<   ",
    " _/ /    / /    / ___ | / /| |  ",
    "/___/   /_/    /_/  |_|/_/ |_|  ",
]

ITAK_LOGO_TECH = [
    "╔╗╔╦══╦══╗╔═╗",
    "║║║╠╗╔╣╔╗║║╔╝",
    "║║║║║║║╠╣║║╚╗",
    "║╚╝║║║║║║║║╔╝",
    "╚══╝╚╝╚╝╚╝╚╝ ",
]

ITAK_LOGO_MINI = [
    "I T A K"
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

# Map styles to variables
LOGO_STYLES = {
    "large": ITAK_LOGO_LARGE,
    "cyber": ITAK_LOGO_CYBER,
    "modern": ITAK_LOGO_MODERN,
    "pixel": ITAK_LOGO_PIXEL,
    "shadow": ITAK_LOGO_SHADOW,
    "dash_3d": ITAK_LOGO_DASH_3D,
    "3d": ITAK_LOGO_3D,
    "slant": ITAK_LOGO_SLANT,
    "tech": ITAK_LOGO_TECH,
    "mini": ITAK_LOGO_MINI,
    "block": ITAK_LOGO_BLOCK,
    "small": ITAK_LOGO
}


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

def colorize_string_horizontally(line: str, colors: List[str]) -> str:
    """Apply gradient colors character by character (Horizontal Fade)."""
    result = ""
    for i, char in enumerate(line):
        if i < len(colors):
            result += f"{colors[i]}{char}"
        else:
            result += f"{colors[-1]}{char}"
    return f"{BOLD}{result}{RESET}"

def print_banner(style: str = "dash_3d", theme_key: str = None):
    """Print the iTaK banner with horizontal smooth gradient."""
    
    # Select Logo
    if style in LOGO_STYLES:
        logo = LOGO_STYLES[style]
    else:
        logo = LOGO_STYLES["dash_3d"]

    # Select Theme
    theme_key = theme_key or CURRENT_THEME
    if theme_key not in THEMES:
         theme_key = CURRENT_THEME
         
    start_hex, end_hex = THEMES[theme_key]
    
    # Calculate Max Width for Gradient Steps
    max_width = max(len(line) for line in logo)
    
    # Generate Horizontal Gradient (Steps = Width)
    colors = generate_gradient_colors(start_hex, end_hex, max_width)
    
    print()
    for line in logo:
        # Render each line with the horizontal gradient map
        print(colorize_string_horizontally(line, colors))
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


def animate_intro(theme_key: str = CURRENT_THEME):
    """Display the wizard and ITAK logo."""
    # Setup Colors
    if theme_key not in THEMES: theme_key = CURRENT_THEME
    start_hex, end_hex = THEMES[theme_key]
    
    # Wizard uses same colors as logo
    wizard_colors = generate_gradient_colors(start_hex, end_hex, 60)
    
    # Print wizard first
    print()
    for line in WIZARD_ASCII:
        print(colorize_string_horizontally(line, wizard_colors))
    
    # Build ITAK logo without arrow
    logo = join_art(D3D_I, D3D_T, D3D_A, D3D_K)
    
    # Calculate colors for logo width
    max_width = max(len(line) for line in logo)
    colors = generate_gradient_colors(start_hex, end_hex, max_width if max_width > 0 else 1)
    
    # Render Logo
    for line in logo:
        print(colorize_string_horizontally(line, colors))
    print()


def print_menu():
    """Print the interactive CLI menu."""
    print(f"\n   {BOLD}What would you like to do?{RESET}\n")
    
    print(f"    [{Theme.CYAN}1{RESET}] 🧙 {Theme.CYAN}Wizard Code{RESET}       {DIM}Create a new project{RESET}")
    print(f"    [{Theme.CYAN}2{RESET}] 💬 {Theme.CYAN}Chat{RESET}              {DIM}General coding help{RESET}")
    print()
    print(f"    [{Theme.CYAN}3{RESET}] ⚡ {Theme.CYAN}API Gateway{RESET}       {DIM}FastAPI & tunnels{RESET}")
    print(f"    [{Theme.CYAN}4{RESET}] 🧩 {Theme.CYAN}Optional Services{RESET} {DIM}Supabase, ComfyUI, etc{RESET}")
    print()

# ... (Existing animate_intro) ...

# --- MAIN (GALLERY) ---
if __name__ == "__main__":
    
    # 1. Animation (Blinking Arrow) - ENABLED
    animate_intro("7. Miami Sunset")
    
    # 2. Main Logo (Dashed 3D Style > ITAK)
    print_banner(style="dash_3d", theme_key="7. Miami Sunset")
    
    # 3. Menu
    print_menu()
    
    # Keep the script running to hold the visual if needed, 
    # but for now just exit so user can see the print.
    print()
