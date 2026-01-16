"""
iTaK Stacked Diffs - Advanced Git Workflow

Implements the Stacked Diffs pattern for managing complex changesets.
Each logical change gets its own branch, stacked on dependencies.

Based on git_client.py from iTaK's this.md specification.
"""

import subprocess
import json
from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class StackedBranch:
    """Represents a branch in a stack."""
    name: str
    base: str
    description: str
    status: str = "active"  # active, merged, abandoned


@dataclass
class DiffStack:
    """Manages a stack of branches for incremental development."""
    name: str
    branches: List[StackedBranch] = field(default_factory=list)
    
    def add_branch(self, branch: StackedBranch) -> None:
        self.branches.append(branch)
    
    def get_current_head(self) -> Optional[str]:
        if not self.branches:
            return None
        return self.branches[-1].name


def run_git(args: List[str], cwd: str = ".") -> tuple[bool, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        return result.returncode == 0, result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return False, str(e)


def get_current_branch(cwd: str = ".") -> Optional[str]:
    """Get the current git branch name."""
    success, output = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    return output if success else None


def create_stacked_branch(
    name: str,
    description: str,
    base: Optional[str] = None,
    cwd: str = ".",
) -> bool:
    """Create a new branch in the stack.
    
    Args:
        name: Branch name (e.g., "feature/add-auth")
        description: Description of the change
        base: Base branch (defaults to current branch)
        cwd: Working directory
        
    Returns:
        True if branch was created successfully
    """
    if base is None:
        base = get_current_branch(cwd)
    
    print(f"📚 STACKED DIFFS: Creating branch '{name}' based on '{base}'")
    
    # Create branch
    success, output = run_git(["checkout", "-b", name], cwd)
    if not success:
        print(f"❌ Failed to create branch: {output}")
        return False
    
    # Create empty commit with description
    success, output = run_git(["commit", "--allow-empty", "-m", f"[STACK] {description}"], cwd)
    if not success:
        print(f"⚠️ Failed to create description commit: {output}")
    
    print(f"✅ Created stacked branch: {name}")
    return True


def commit_to_stack(message: str, files: List[str] = None, cwd: str = ".") -> bool:
    """Commit changes to the current stack branch.
    
    Args:
        message: Commit message
        files: Specific files to add (None = all changes)
        cwd: Working directory
        
    Returns:
        True if commit was successful
    """
    # Add files
    if files:
        for f in files:
            run_git(["add", f], cwd)
    else:
        run_git(["add", "-A"], cwd)
    
    # Commit
    success, output = run_git(["commit", "-m", message], cwd)
    if not success:
        print(f"❌ Commit failed: {output}")
        return False
    
    print(f"✅ Committed: {message}")
    return True


def sync_stack(base_branch: str = "main", cwd: str = ".") -> bool:
    """Rebase the current stack on the base branch.
    
    This updates the stack to include the latest changes from the base.
    
    Args:
        base_branch: The branch to rebase onto
        cwd: Working directory
        
    Returns:
        True if rebase was successful
    """
    current = get_current_branch(cwd)
    print(f"🔄 SYNC: Rebasing '{current}' onto '{base_branch}'...")
    
    # Fetch latest
    run_git(["fetch", "origin", base_branch], cwd)
    
    # Rebase
    success, output = run_git(["rebase", f"origin/{base_branch}"], cwd)
    if not success:
        print(f"⚠️ Rebase conflict: {output}")
        print("   Resolve conflicts and run 'git rebase --continue'")
        return False
    
    print(f"✅ Stack synced with {base_branch}")
    return True


def push_stack(force: bool = False, cwd: str = ".") -> bool:
    """Push the current stack branch to remote.
    
    Args:
        force: Force push (use with caution)
        cwd: Working directory
        
    Returns:
        True if push was successful
    """
    branch = get_current_branch(cwd)
    args = ["push", "-u", "origin", branch]
    if force:
        args.insert(1, "--force-with-lease")
    
    success, output = run_git(args, cwd)
    if not success:
        print(f"❌ Push failed: {output}")
        return False
    
    print(f"✅ Pushed: {branch}")
    return True


def list_stack_branches(prefix: str = "stack/", cwd: str = ".") -> List[str]:
    """List all branches in the stack.
    
    Args:
        prefix: Branch prefix to filter
        cwd: Working directory
        
    Returns:
        List of branch names
    """
    success, output = run_git(["branch", "--list", f"{prefix}*"], cwd)
    if not success:
        return []
    
    branches = [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]
    return branches


def squash_stack(target_branch: str = "main", cwd: str = ".") -> bool:
    """Squash all stack commits into a single commit on target.
    
    This is the final step when landing a stack - combines all the
    incremental commits into a clean merge.
    
    Args:
        target_branch: Branch to merge into
        cwd: Working directory
        
    Returns:
        True if squash was successful
    """
    current = get_current_branch(cwd)
    
    print(f"🎯 LANDING: Squashing '{current}' into '{target_branch}'...")
    
    # Checkout target
    success, _ = run_git(["checkout", target_branch], cwd)
    if not success:
        return False
    
    # Pull latest
    run_git(["pull", "origin", target_branch], cwd)
    
    # Squash merge
    success, output = run_git(["merge", "--squash", current], cwd)
    if not success:
        print(f"❌ Squash merge failed: {output}")
        run_git(["checkout", current], cwd)
        return False
    
    print(f"✅ Stack squashed. Ready for final commit.")
    return True


def create_snapshot_branch(label: str = "snapshot", cwd: str = ".") -> bool:
    """Create a snapshot branch for backup before destructive operations.
    
    Follows iTaK principle: 'Snapshot Before Destruction'
    
    Args:
        label: Label for the snapshot
        cwd: Working directory
        
    Returns:
        True if snapshot was created
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"snapshot/{label}_{timestamp}"
    
    success, _ = run_git(["branch", snapshot_name], cwd)
    if success:
        print(f"📸 Snapshot created: {snapshot_name}")
    return success


if __name__ == "__main__":
    print("iTaK Stacked Diffs - Git Workflow Tool")
    print(f"Current branch: {get_current_branch()}")
    print(f"Stack branches: {list_stack_branches()}")
