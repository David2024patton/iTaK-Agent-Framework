# PR: Scaffold Electron Desktop Application - OpenClaw

## Overview

This PR scaffolds a complete Electron desktop application that wraps the iTaK Agent Framework Python CLI, providing both a graphical interface and system-wide terminal access.

## Key Features

### 1. **In-Process CLI Integration (Option B)**
- Spawns Python CLI as child process from Electron main process
- Safe subprocess management that prevents `process.exit` from terminating Electron
- Real-time log streaming from CLI to renderer UI
- Programmatic control APIs (start/stop/runCommand)

### 2. **Cross-Platform Installers with CLI Shim**
- **macOS DMG**: Installs to `/Applications`, creates `/usr/local/bin/openclaw` launcher
- **Windows NSIS**: Installs to Program Files, creates `openclaw.cmd` and adds to PATH
- **Linux AppImage/DEB**: Creates `/usr/local/bin/openclaw` via postinstall script

### 3. **React Dashboard UI**
- Modern dark theme interface
- Real-time log viewer with auto-scroll
- Agent control (start/stop buttons)
- CLI command execution
- Onboarding flow for first-time users
- Branded with OpenClaw logo

### 4. **Safety Features**
- Process exit protection prevents CLI from killing Electron
- Exit attempts logged and displayed in UI
- Error handling for missing Python/dependencies
- Subprocess cleanup on app quit

## Architecture

```
apps/electron/
├── src/
│   ├── main/
│   │   └── main.ts              # Electron main process, window management, IPC setup
│   ├── preload/
│   │   └── preload.ts           # contextBridge API exposure
│   ├── renderer/
│   │   ├── App.tsx              # React dashboard UI
│   │   ├── index.html           # HTML entry point
│   │   └── styles.css           # Dark theme styles
│   └── electron-adapter.ts      # Python CLI wrapper with safety features
├── scripts/
│   ├── installer.nsh            # Windows NSIS custom install script
│   └── postinstall.sh           # Linux deb postinstall script
├── assets/                      # Placeholder icons (to be replaced)
├── package.json                 # Dependencies and build scripts
├── tsconfig.main.json           # TypeScript config for main/preload
├── tsconfig.renderer.json       # TypeScript config for renderer
├── vite.config.ts               # Vite bundler config
└── README.md                    # Developer documentation
```

## electron-adapter.ts Implementation

The adapter is the core integration point:

1. **Python Detection**: Auto-detects `python3`, `python`, or `py` commands
2. **Resource Path Handling**: Switches between dev (repo root) and production (bundled resources)
3. **Process Exit Protection**: Patches `process.exit` to emit events instead of exiting
4. **Subprocess Management**: 
   - `startAgent()`: Launches interactive CLI mode
   - `stopAgent()`: Graceful termination with SIGTERM/SIGKILL fallback
   - `runCommand(args)`: Executes one-off CLI commands
   - `sendInput(input)`: Sends input to running agent
5. **Event Emitters**: Forwards logs, exit attempts, and status changes to renderer

## IPC API Surface

Exposed via `window.openclaw` in renderer:

```typescript
interface OpenClawAPI {
  startAgent(): Promise<CommandResult>;
  stopAgent(): Promise<CommandResult>;
  runCommand(args: string[]): Promise<CommandResult>;
  getStatus(): Promise<Status>;
  sendInput(input: string): Promise<boolean>;
  onLog(callback): UnsubscribeFn;
  onExitAttempt(callback): UnsubscribeFn;
  onAgentStopped(callback): UnsubscribeFn;
}
```

## Build Process

### Development
```bash
npm run electron:dev
```
- Builds main process and renderer
- Launches Electron with DevTools
- Watches for changes

### Production
```bash
npm run electron:build    # Build TypeScript and React
npm run electron:dist     # Create installers for current platform
npm run electron:dist:mac # macOS only
npm run electron:dist:win # Windows only  
npm run electron:dist:linux # Linux only
```

## CLI Shim Behavior

After installation, users can run:
```bash
openclaw --version
openclaw --help
openclaw create crew my-crew
# ... any iTaK CLI command
```

The shim works differently per platform:

### macOS
- Shell script at `/usr/local/bin/openclaw`
- Executes: `/Applications/OpenClaw.app/Contents/MacOS/OpenClaw --headless "$@"`
- Requires admin during install (creates symlink in /usr/local/bin)

### Windows
- Batch file `openclaw.cmd` in installation directory
- Installation directory added to system PATH
- Executes: `OpenClaw.exe --headless %*`
- Requires admin during install (modifies system PATH)

### Linux
- Shell script at `/usr/local/bin/openclaw`
- Created by postinstall script in .deb package
- Executes: `/opt/OpenClaw/openclaw --headless "$@"`
- Requires sudo for .deb installation

## Python/Node Compatibility

### Python Requirements
- Python 3.10-3.13 (iTaK framework requirements)
- iTaK dependencies installed via pip

### Node/Electron Requirements
- Node.js 16+ (specified in root package.json)
- Electron 28.x (recent stable LTS)
- TypeScript 5.3+
- Vite 5.x for renderer bundling

The Electron adapter automatically detects the Python executable, so no manual configuration needed.

## GitHub Actions Workflow

`.github/workflows/electron-build.yml` runs on:
- Push to `main` branch (when electron files change)
- Pull requests affecting electron directory
- Manual workflow dispatch

**Build matrix**: ubuntu-latest, macos-latest, windows-latest

**Steps**:
1. Setup Node.js and Python
2. Install Python dependencies (iTaK framework)
3. Install Electron dependencies
4. Build application
5. Type check TypeScript
6. Create platform-specific installers
7. Upload artifacts (30-day retention)

## Testing Checklist

### Manual Testing Required
- [ ] Install on macOS - verify DMG install and CLI shim
- [ ] Install on Windows - verify NSIS install and PATH registration
- [ ] Install on Linux - verify .deb install and postinstall script
- [ ] Test `openclaw` command in terminal after install
- [ ] Test UI: start/stop agent
- [ ] Test UI: run CLI commands
- [ ] Test UI: log streaming
- [ ] Verify process.exit protection (CLI shouldn't crash Electron)

### Automated Testing
- [x] TypeScript compilation (main process)
- [x] TypeScript compilation (renderer)
- [x] Vite build (renderer bundle)
- [ ] GitHub Actions build (will run on push)

## Known Limitations & Future Work

### Current Limitations
1. **Placeholder Icons**: Icon files are empty placeholders. Need to create actual icon files from OpenClaw logo.
2. **--headless Flag**: The CLI shim invokes with `--headless` flag which may need to be implemented in iTaK CLI (or adjusted to match actual CLI behavior).
3. **Python Path**: Assumes Python is in PATH. May need bundled Python for true standalone distribution.

### Future Enhancements
1. **Auto-updates**: Implement electron-updater for OTA updates
2. **Tray Icon**: Add system tray with quick controls
3. **Configuration UI**: GUI for iTaK settings/configuration
4. **Bundled Python**: Include Python runtime for fully standalone app
5. **Code Signing**: Add certificate signing for macOS/Windows
6. **Notarization**: macOS notarization for Gatekeeper
7. **Real Icon Assets**: Create professional icons from branding

## Changes to Repository

### New Files
- `apps/electron/` - Entire Electron application directory
- `.github/workflows/electron-build.yml` - CI workflow

### Modified Files
- `package.json` - Added electron scripts
- `.gitignore` - Added electron build artifacts

### No Changes to Existing Code
- iTaK Python CLI code unchanged
- No modifications to existing package structure
- Electron app is additive only

## Security Considerations

1. **Process Exit Protection**: Prevents malicious or buggy CLI code from terminating Electron
2. **Context Isolation**: Renderer runs with contextIsolation enabled
3. **No Node Integration**: Renderer has no direct Node.js access
4. **IPC Sandboxing**: All CLI access goes through validated IPC handlers
5. **Subprocess Isolation**: Python runs as separate process, can be killed without affecting Electron

## Developer Notes

### Before Running Electron App
The Python iTaK framework must be installed:
```bash
pip install -e .
```

### Recommended Electron Version
Electron 28.x uses Node 18.x, which meets the repository's Node >=16.0.0 requirement.

### Adding Real Icons
Replace placeholder files in `apps/electron/assets/`:
- `icon.icns` - macOS icon (use `iconutil` to convert PNG)
- `icon.ico` - Windows icon (multi-resolution)
- `icon.png` - Linux icon (512x512 PNG)

Use the OpenClaw logo: https://mintcdn.com/clawdhub/FaXdIfo7gPK_jSWb/assets/openclaw-logo-text.png

### Debugging
Development mode opens DevTools automatically. Check:
- Console for adapter logs
- Network tab for IPC messages
- Application tab for storage

## Questions & Feedback

This is an initial scaffold. Please review:
1. Is the `--headless` flag approach acceptable for CLI invocation?
2. Should we bundle Python runtime or rely on system Python?
3. Are the installer permissions (admin/sudo) acceptable?
4. Should we add auto-update functionality now or later?
5. Any changes needed to iTaK CLI exports for better integration?

## PR Review Checklist

- [x] Code compiles without errors
- [x] TypeScript strict mode enabled
- [x] All files have consistent formatting
- [x] Documentation complete (README)
- [x] .gitignore updated
- [x] CI workflow added
- [ ] Manual testing on all platforms
- [ ] Code review feedback addressed
- [ ] Security scan passed
