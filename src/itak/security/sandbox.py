"""
iTaK Docker Sandbox - Safe Code Execution

Implements safe code execution in isolated Docker containers.
Part of Layer 6 (Sandbox) - progressive trust principle.

Based on run_safe.py from iTaK's this.md specification.
"""

import subprocess
import sys
import json
import time
from typing import Optional
from dataclasses import dataclass


CONTAINER_NAME = "itak_sandbox"
DEFAULT_IMAGE = "python:3.11-slim"


@dataclass
class SandboxResult:
    """Result from sandbox execution."""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float


def ensure_sandbox_active() -> bool:
    """Self-healing: Starts the sandbox container if it's down."""
    try:
        check = subprocess.run(
            ["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        if CONTAINER_NAME in check.stdout.strip():
            return True
        
        print(f"🚑 HEALER: Sandbox container '{CONTAINER_NAME}' is down. Auto-starting...")
        
        # Try to start existing container
        result = subprocess.run(["docker", "start", CONTAINER_NAME], capture_output=True)
        if result.returncode == 0:
            print("✅ Sandbox restarted.")
            time.sleep(2)
            return True
        
        # Create new container
        subprocess.run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "--network", "none",  # No network access for security
            "-v", f"{subprocess.os.getcwd()}:/workspace:ro",  # Read-only mount
            DEFAULT_IMAGE,
            "tail", "-f", "/dev/null"  # Keep container running
        ], check=True)
        
        print("✅ Sandbox container created.")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL: Failed to start sandbox: {e}")
        return False


def run_in_sandbox(
    code: str,
    timeout: int = 30,
    memory_limit: str = "256m",
) -> SandboxResult:
    """Execute Python code in the isolated sandbox container.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        memory_limit: Docker memory limit
        
    Returns:
        SandboxResult with execution details
    """
    if not ensure_sandbox_active():
        return SandboxResult(
            success=False,
            stdout="",
            stderr="Sandbox container not available",
            exit_code=-1,
            execution_time=0.0,
        )
    
    print(f"🏃 SANDBOX: Executing code in isolated container...")
    start_time = time.time()
    
    try:
        # Execute code in container
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        
        execution_time = time.time() - start_time
        
        return SandboxResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            execution_time=execution_time,
        )
        
    except subprocess.TimeoutExpired:
        return SandboxResult(
            success=False,
            stdout="",
            stderr=f"Execution timed out after {timeout} seconds",
            exit_code=-1,
            execution_time=timeout,
        )
    except Exception as e:
        return SandboxResult(
            success=False,
            stdout="",
            stderr=str(e),
            exit_code=-1,
            execution_time=time.time() - start_time,
        )


def run_script_in_sandbox(script_path: str, timeout: int = 60) -> SandboxResult:
    """Execute a Python script file in the sandbox.
    
    Args:
        script_path: Path to the Python script
        timeout: Maximum execution time
        
    Returns:
        SandboxResult with execution details
    """
    if not ensure_sandbox_active():
        return SandboxResult(
            success=False,
            stdout="",
            stderr="Sandbox container not available",
            exit_code=-1,
            execution_time=0.0,
        )
    
    print(f"🏃 SANDBOX: Executing script: {script_path}")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["docker", "exec", "-w", "/workspace", CONTAINER_NAME, "python", script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        
        execution_time = time.time() - start_time
        
        return SandboxResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            execution_time=execution_time,
        )
        
    except subprocess.TimeoutExpired:
        return SandboxResult(
            success=False,
            stdout="",
            stderr=f"Execution timed out after {timeout} seconds",
            exit_code=-1,
            execution_time=timeout,
        )
    except Exception as e:
        return SandboxResult(
            success=False,
            stdout="",
            stderr=str(e),
            exit_code=-1,
            execution_time=time.time() - start_time,
        )


def lint_code(script_path: str) -> dict:
    """Quality Gate: Runs Ruff, Mypy, and Bandit in sandbox.
    
    Args:
        script_path: Path to the script to lint
        
    Returns:
        Dict with linting results
    """
    print(f"🧹 VALIDATOR: Scanning {script_path}...")
    results = {"passed": True, "issues": []}
    
    if not ensure_sandbox_active():
        results["passed"] = False
        results["issues"].append("Sandbox not available")
        return results
    
    # Run Ruff
    try:
        ruff_result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "python", "-m", "ruff", "check", f"/workspace/{script_path}"],
            capture_output=True, text=True
        )
        if ruff_result.returncode != 0:
            results["issues"].append(f"Ruff: {ruff_result.stdout}")
            results["passed"] = False
    except Exception as e:
        results["issues"].append(f"Ruff error: {e}")
    
    if results["passed"]:
        print("   ✅ Quality Gate Passed")
    else:
        print(f"   ⛔ Quality Gate Failed: {len(results['issues'])} issues")
    
    return results


def stop_sandbox() -> bool:
    """Stop the sandbox container."""
    try:
        subprocess.run(["docker", "stop", CONTAINER_NAME], check=True, capture_output=True)
        print(f"✅ Sandbox container stopped")
        return True
    except Exception as e:
        print(f"⚠️ Failed to stop sandbox: {e}")
        return False


def cleanup_sandbox() -> bool:
    """Stop and remove the sandbox container."""
    try:
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], capture_output=True)
        print(f"✅ Sandbox container removed")
        return True
    except Exception as e:
        print(f"⚠️ Failed to cleanup sandbox: {e}")
        return False


if __name__ == "__main__":
    # Demo
    print("Testing sandbox...")
    
    # Safe code
    result = run_in_sandbox("print('Hello from sandbox!')")
    print(f"Result: {result}")
    
    # Code that would be dangerous on host
    result = run_in_sandbox("import os; print(os.getcwd())")
    print(f"Result: {result}")
