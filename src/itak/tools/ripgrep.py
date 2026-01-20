import os
import shutil
import subprocess
import json
import logging
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel, Field
from itak.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class RipGrepSearch:
    """
    High-performance code search using ripgrep (rg).
    Ported from gemini-cli's `ripGrep.ts`.
    """
    
    def __init__(self, bin_dir: Optional[str] = None):
        self.bin_dir = bin_dir or os.path.expanduser("~/.itak/bin")
        self.rg_path = self._find_binary()

    def _find_binary(self) -> Optional[str]:
        # 1. Check Module-specific bin dir
        if os.path.exists(self.bin_dir):
            candidate = os.path.join(self.bin_dir, "rg.exe" if os.name == 'nt' else "rg")
            if os.path.exists(candidate):
                return candidate
                
        # 2. Check System PATH
        system_rg = shutil.which("rg")
        if system_rg:
            return system_rg
            
        return None

    def is_available(self) -> bool:
        return self.rg_path is not None

    def search(
        self, 
        pattern: str, 
        path: str = ".", 
        case_sensitive: bool = False,
        fixed_strings: bool = False,
        glob_include: Optional[str] = None,
        context: int = 0
    ) -> Dict[str, Any]:
        
        if not self.rg_path:
            return {
                "success": False, 
                "error": "ripgrep (rg) binary not found. Please install it or run 'itak setup ripgrep'."
            }

        cmd = [self.rg_path, "--json"]
        
        if not case_sensitive:
            cmd.append("--ignore-case")
            
        if fixed_strings:
            cmd.append("--fixed-strings")
        
        if context > 0:
            cmd.extend(["--context", str(context)])
            
        if glob_include:
            cmd.extend(["--glob", glob_include])
            
        # Add pattern and path
        cmd.extend(["--", pattern, path])
        
        try:
            # Run process
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='replace'
            )
        except Exception as e:
             return {"success": False, "error": f"Failed to execute rg: {str(e)}"}

        matches = []
        parse_errors = 0
        
        # Parse JSON Lines output
        for line in result.stdout.splitlines():
            try:
                data = json.loads(line)
                if data['type'] == 'match':
                    matches.append({
                        "file": data['data']['path']['text'],
                        "line_number": data['data']['line_number'],
                        "content": data['data']['lines']['text'].rstrip()
                    })
            except json.JSONDecodeError:
                parse_errors += 1
                
        return {
            "success": True,
            "count": len(matches),
            "matches": matches[:1000], # Hard cap for now
            "truncated": len(matches) > 1000
        }

    def install_instructions(self) -> str:
        if os.name == 'nt':
            return "winget install BurntSushi.ripgrep.MSVC"
        else:
            return "sudo apt-get install ripgrep"


class RipGrepInput(BaseModel):
    """Input schema for RipGrepTool."""
    pattern: str = Field(..., description="The search pattern (regex by default, or string if fixed_strings=True).")
    path: str = Field(".", description="The path to search in (file or directory). Defaults to current directory.")
    case_sensitive: bool = Field(False, description="Whether the search should be case sensitive.")
    fixed_strings: bool = Field(False, description="Treat the pattern as a literal string instead of a regex.")
    glob_include: Optional[str] = Field(None, description="Glob pattern to include files (e.g. '*.py').")
    context: int = Field(0, description="Number of context lines to include around matches.")

class RipGrepTool(BaseTool):
    name: str = "RipGrep"
    description: str = (
        "A fast code search tool using ripgrep. "
        "Use this for finding code snippets, function definitions, or references across the codebase. "
        "It is much faster than standard file reading."
    )
    args_schema: Type[BaseModel] = RipGrepInput

    def _run(
        self, 
        pattern: str, 
        path: str = ".", 
        case_sensitive: bool = False, 
        fixed_strings: bool = False,
        glob_include: Optional[str] = None,
        context: int = 0
    ) -> str:
        rg = RipGrepSearch()
        result = rg.search(pattern, path, case_sensitive, fixed_strings, glob_include, context)
        
        if not result["success"]:
            return f"Search Error: {result['error']}"
            
        if result["count"] == 0:
            return "No matches found."
            
        output = [f"Found {result['count']} matches:"]
        for match in result["matches"]:
            output.append(f"{match['file']}:{match['line_number']}  {match['content']}")
            
        if result.get("truncated"):
            output.append("... (results truncated)")
            
        return "\n".join(output)
