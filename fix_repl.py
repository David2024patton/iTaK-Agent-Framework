import sys

# Read repl.py
with open(r'd:\test\testing\src\itak\cli\repl.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 99: "from .wizard import run_project_wizard"
# Replace with: "from .wizard import run_project_wizard, ExitCLI"

for i, line in enumerate(lines):
    if 'from .wizard import run_project_wizard' in line and i < 110:
        lines[i] = '                from .wizard import run_project_wizard, ExitCLI\r\n'
        print(f"✅ Updated import on line {i+1}")
        break

# Find the exception handling around line 103-106
# Add ExitCLI exception handler before ImportError

for i in range(len(lines)):
    if i > 100 and 'except ImportError:' in lines[i] and 'wizard' in lines[i-5:i+1][-1].lower():
        # Insert ExitCLI handler before this line
        indent = '            '
        new_lines = [
            f'{indent}except ExitCLI:\r\n',
            f'{indent}    # User wants to exit CLI completely, don\'t restart menu\r\n',
            f'{indent}    print(f"\\n{{YELLOW}}Goodbye!{{RESET}}\\n")\r\n',
            f'{indent}    return\r\n',
        ]
        lines[i:i] = new_lines
        print(f"✅ Added ExitCLI handler before line {i+1}")
        break

# Write back
with open(r'd:\test\testing\src\itak\cli\repl.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ repl.py updated successfully")
