import sys

# Read the file
with open(r'd:\test\testing\src\itak\cli\wizard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the description section (around line 107-111)
# We need to replace:
#         else:
#             description = wizard_prompt("  What should it do", default_desc)
#
# With:
#         else:
#             # Force user to enter a description (required for auto-detection)
#             while True:
#                 description = wizard_prompt("  What should it do", default_desc)
#                 if description.strip():  # Non-empty after stripping whitespace
#                     break
#                 click.secho("  ⚠️  Please describe what your project should do", fg="yellow")
#                 click.echo()

new_section = [
    '        else:\r\n',
    '            # Force user to enter a description (required for auto-detection)\r\n',
    '            while True:\r\n',
    '                description = wizard_prompt("  What should it do", default_desc)\r\n',
    '                if description.strip():  # Non-empty after stripping whitespace\r\n',
    '                    break\r\n',
    '                click.secho("  ⚠️  Please describe what your project should do", fg="yellow")\r\n',
    '                click.echo()\r\n',
]

# Replace lines 110-111 (0-indexed: 109-110)
lines[109:111] = new_section

# Write back
with open(r'd:\test\testing\src\itak\cli\wizard.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Validation loop added successfully")
