---
description: Browser automation for AI agents using Vercel's agent-browser CLI
---

# Agent Browser Skill

Browser automation CLI optimized for AI agents. Uses Playwright under the hood but provides 95% first-try success rate vs 80% for Playwright MCP.

## Installation

```bash
npm install -g @anthropic-ai/agent-browser
```

For Linux/WSL:
```bash
npx playwright install-deps
```

## Core Concepts

### Refs (Reference IDs)
When you take a snapshot, the CLI returns a condensed accessibility tree with refs like `@e1`, `@e2`, etc. Use these to interact with elements.

### Agent Mode
Always use `--json` for machine-readable output:
```bash
agent-browser <command> --json
```

## Essential Commands

### Navigate and Snapshot
```bash
# Navigate to a URL
agent-browser goto "https://example.com"

# Take a snapshot (returns refs for all interactable elements)
agent-browser snapshot --json

# Take a screenshot
agent-browser screenshot --path "screenshot.png"
```

### Interact with Elements
```bash
# Click an element by ref
agent-browser click @e1

# Fill a text field
agent-browser fill @e2 "text to enter"

# Get text content
agent-browser get text @e1

# Check if visible
agent-browser is visible @e1
```

### Wait Commands
```bash
# Wait for element to appear
agent-browser wait @e1

# Wait for navigation
agent-browser wait navigation

# Wait for network idle
agent-browser wait network-idle
```

### Mouse Control
```bash
# Hover over element
agent-browser hover @e1

# Scroll
agent-browser scroll down
agent-browser scroll up
agent-browser scroll @e1
```

## Optimal AI Workflow

1. **Navigate**: `agent-browser goto "URL"`
2. **Snapshot**: `agent-browser snapshot --json` → Get refs
3. **Analyze**: Review refs to find target elements
4. **Act**: Use refs to click, fill, etc.
5. **Verify**: Take screenshot or check visibility
6. **Repeat**: Take new snapshot if page changed

## Example: Form Submission

```bash
# 1. Navigate
agent-browser goto "https://example.com/login"

# 2. Get page structure
agent-browser snapshot --json
# Returns: {"refs": {"e1": {"role": "textbox", "name": "Email"}, "e2": {"role": "textbox", "name": "Password"}, "e3": {"role": "button", "name": "Sign In"}}}

# 3. Fill form
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"

# 4. Submit
agent-browser click @e3

# 5. Wait and verify
agent-browser wait navigation
agent-browser screenshot --path "after_login.png"
```

## Example: Site Validation

```bash
# Navigate to site
agent-browser goto "http://localhost:3000"

# Take snapshot for analysis
agent-browser snapshot --json

# Check key elements exist
agent-browser is visible @e1 --json  # Header
agent-browser is visible @e5 --json  # Navigation

# Click through pages
agent-browser click @e3  # About link
agent-browser wait navigation
agent-browser screenshot --path "about_page.png"

# Test form
agent-browser fill @e10 "Test input"
agent-browser click @e11  # Submit
```

## Tips

1. **Always use `--json`** for parseable output
2. **Take snapshots after navigation** - page state changes
3. **Use refs, not selectors** - more reliable
4. **Take screenshots for verification** - artifacts for review
5. **Works best on Linux/WSL** - Windows has issues

## Why This is Better Than Playwright MCP

| Issue | Playwright MCP | agent-browser |
|-------|---------------|---------------|
| Non-deterministic matching | ❌ Common | ✅ Uses refs |
| Context size | ❌ Large accessibility tree | ✅ Condensed refs |
| First-try success | 80% | **95%** |
| Token efficiency | Poor | Excellent |

## Session Management

```bash
# Sessions persist between commands
agent-browser goto "https://example.com"  # Session starts
agent-browser click @e1                    # Same session
agent-browser close                        # End session
```
