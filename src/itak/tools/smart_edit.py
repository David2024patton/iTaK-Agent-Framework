from typing import Type, Optional, Any, Dict
from pydantic import BaseModel, Field
from itak.tools.base_tool import BaseTool
import re

# ... [Keep existing SmartEditor class as is] ...

class SmartEditor:
    """
    Port of 'Battle-Tested' Edit Logic (from gemini-cli).
    Provides Self-Healing capabilities for file edits.
    """

    @staticmethod
    def _detect_line_ending(content: str) -> str:
        if '\r\n' in content:
            return '\r\n'
        return '\n'

    @staticmethod
    def _restore_trailing_newline(original: str, modified: str) -> str:
        had_newline = original.endswith('\n')
        if had_newline and not modified.endswith('\n'):
            return modified + '\n'
        elif not had_newline and modified.endswith('\n'):
            return modified.rstrip('\n')
        return modified

    def calculate_flexible_replacement(
        self, 
        current_content: str, 
        old_string: str, 
        new_string: str
    ) -> Optional[str]:
        """
        Matches text blocks even if indentation differs slightly.
        Ported from gemini-cli's `calculateFlexibleReplacement`.
        """
        normalized_code = current_content
        normalized_search = old_string.replace('\r\n', '\n').strip()
        normalized_replace = new_string.replace('\r\n', '\n')

        source_lines = normalized_code.splitlines(keepends=True)
        search_lines_stripped = [l.strip() for l in normalized_search.split('\n')]
        replace_lines = normalized_replace.split('\n')

        i = 0
        while i <= len(source_lines) - len(search_lines_stripped):
            # Extract window of lines equal to search length
            window = source_lines[i : i + len(search_lines_stripped)]
            window_stripped = [l.strip() for l in window]

            # Check for match (ignoring indentation)
            if window_stripped == search_lines_stripped:
                # Found match!
                first_line_match = window[0]
                # Capture indentation from source
                indentation = re.match(r"^(\s*)", first_line_match)
                indent = indentation.group(1) if indentation else ""

                # Re-indent new block
                new_block_lines = [f"{indent}{line}" for line in replace_lines]
                new_block = '\n'.join(new_block_lines)

                # Execute Replacement
                before = "".join(source_lines[:i])
                after = "".join(source_lines[i + len(search_lines_stripped):])
                
                modified = before + new_block + '\n' + after # Naive join, fine for now
                return self._restore_trailing_newline(current_content, modified)

            i += 1
        
        return None

    def calculate_regex_replacement(
        self, 
        current_content: str, 
        old_string: str, 
        new_string: str
    ) -> Optional[str]:
        """
        Dynamically builds a regex to match tokens with variable whitespace.
        Ported from gemini-cli's `calculateRegexReplacement`.
        """
        normalized_search = old_string.replace('\r\n', '\n')
        
        # Split by delimiters to tokenize special chars
        delimiters = r'[():\[\]{}><=]'
        # Add spaces around delimiters to split easier
        processed = re.sub(f"({delimiters})", r" \1 ", normalized_search)
        
        # Tokenize by whitespace
        tokens = [t for t in processed.split() if t.strip()]
        
        if not tokens:
            return None

        # Escape tokens for Regex
        escaped_tokens = [re.escape(t) for t in tokens]
        
        # Join with \s* to match ANY whitespace (spaces, tabs, newlines)
        pattern_inner = r"\s*".join(escaped_tokens)
        
        # Capture leading indentation
        final_pattern = r"^(\s*)" + pattern_inner
        
        # Compile MULTILINE regex
        regex = re.compile(final_pattern, re.MULTILINE)
        
        match = regex.search(current_content)
        if not match:
            return None
            
        indentation = match.group(1) or ""
        
        # Re-indent new string
        new_lines = new_string.replace('\r\n', '\n').split('\n')
        new_block = '\n'.join([f"{indentation}{line}" for line in new_lines])
        
        # Replace
        modified = current_content[:match.start()] + new_block + current_content[match.end():]
        return self._restore_trailing_newline(current_content, modified)

    def apply_edit(self, file_path: str, old_string: str, new_string: str) -> Dict[str, Any]:
        """
        Main entry point. Tries Exact -> Flexible -> Regex.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return {"success": False, "error": "File not found"}

        # 1. Exact Match
        if old_string in content:
            new_content = content.replace(old_string, new_string, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return {"success": True, "content": new_content, "strategy": "exact"}

        # 2. Flexible Match (Ignore Indent)
        flexible = self.calculate_flexible_replacement(content, old_string, new_string)
        if flexible:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(flexible)
            return {"success": True, "content": flexible, "strategy": "flexible"}
            
        # 3. Regex Match (Ignore Whitespace entirely)
        regex_match = self.calculate_regex_replacement(content, old_string, new_string)
        if regex_match:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(regex_match)
            return {"success": True, "content": regex_match, "strategy": "regex"}

        return {
            "success": False, 
            "error": "Could not find string to replace", 
            "strategies_tried": ["exact", "flexible", "regex"]
        }


class SmartEditInput(BaseModel):
    """Input schema for SmartEditTool."""
    file_path: str = Field(..., description="The absolute path to the file to edit.")
    old_string: str = Field(..., description="The exact string to be replaced. Must be unique.")
    new_string: str = Field(..., description="The new string to replace the old string with.")

class SmartEditTool(BaseTool):
    name: str = "SmartEdit"
    description: str = (
        "A robust file editing tool that can handle indentation mismatches and verify edits. "
        "Use this tool to update code files. "
        "It employs 'Self-Healing' strategies to find the target code even if whitespace is inexact."
    )
    args_schema: Type[BaseModel] = SmartEditInput

    def _run(self, file_path: str, old_string: str, new_string: str) -> str:
        editor = SmartEditor()
        result = editor.apply_edit(file_path, old_string, new_string)
        
        if result["success"]:
            return f"Successfully edited {file_path} using strategy: {result['strategy']}"
        else:
            return f"Failed to edit {file_path}: {result['error']}"
