import sys

# Read repl.py
with open(r'd:\test\testing\src\itak\cli\repl.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 102: "self.start()" after wizard
# Insert ExitCLI handler BEFORE the ImportError (line 103)

for i, line in enumerate(lines):
    if i > 95 and i < 110 and 'except ImportError:' in line:
        # Check if this is the wizard section
        prev_lines = ''.join(lines[max(0, i-10):i])
        if 'wizard' in prev_lines.lower():
            # Insert ExitCLI handler here
            indent = '            '
            new_handler = [
                f'{indent}except ExitCLI:\r\n',
                f'{indent}    # User wants to exit CLI completely\r\n',
                f'{indent}    print(f"\\n{{YELLOW}}Goodbye!{{RESET}}\\n")\r\n',
                f'{indent}    return\r\n',
            ]
            lines[i:i] = new_handler
            print(f"✅ Added ExitCLI handler at line {i+1}")
            break
else:
    print("❌ Could not find insertion point")
    sys.exit(1)

# Write back
with open(r'd:\test\testing\src\itak\cli\repl.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ repl.py updated successfully")
