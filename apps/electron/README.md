# OpenClaw Desktop Application

Desktop wrapper for the iTaK Agent Framework, providing a graphical interface and system-wide CLI access.

## Overview

OpenClaw Desktop is an Electron-based application that:
- Wraps the Python-based iTaK CLI in a desktop interface
- Provides visual monitoring and control through a React dashboard
- Installs a system-wide `openclaw` command for terminal access
- Safely manages the CLI process without affecting the Electron runtime

## Development Setup

### Prerequisites

- Node.js 16+ (for Electron)
- Python 3.10+ (for iTaK framework)
- npm or pnpm package manager

### Installation

1. Install dependencies:
```bash
cd apps/electron
npm install
```

2. Ensure the parent iTaK project is properly installed:
```bash
cd ../..
pip install -e .
```

### Running in Development

```bash
npm run dev
```

This will:
- Build the main process TypeScript
- Build the renderer with Vite
- Launch Electron with DevTools open

### Building for Distribution

Build all components:
```bash
npm run build
```

Create installer packages:
```bash
# All platforms (if supported)
npm run dist

# Specific platforms
npm run dist:mac   # macOS DMG
npm run dist:win   # Windows NSIS installer
npm run dist:linux # Linux AppImage and DEB
```

## Architecture

### Main Process (`src/main/main.ts`)
- Creates the application window
- Manages IPC communication
- Initializes the Python CLI adapter

### Preload Script (`src/preload/preload.ts`)
- Exposes secure IPC APIs to renderer via contextBridge
- Provides typed interfaces for frontend

### Renderer (`src/renderer/`)
- React-based dashboard UI
- Real-time log streaming
- Agent control (start/stop)
- Command execution interface

### CLI Adapter (`src/electron-adapter.ts`)
- Spawns Python CLI as child process
- Intercepts process.exit to prevent Electron termination
- Streams logs to renderer
- Provides programmatic control APIs

## System-Wide CLI Installation

The installer configures terminal access differently per platform:

### macOS
- Creates symlink in `/usr/local/bin/openclaw`
- Requires administrator privileges during installation
- Accessible immediately after install

### Windows
- Creates `openclaw.cmd` batch wrapper
- Adds installation directory to system PATH
- Requires administrator privileges
- Terminal restart needed after installation

### Linux (Debian/Ubuntu)
- Post-install script creates launcher in `/usr/local/bin/openclaw`
- Works with both AppImage and DEB packages
- May require `sudo` during installation

## Usage

### Desktop Application

Launch from Applications menu or:
```bash
open /Applications/OpenClaw.app  # macOS
# Start menu on Windows
# Application launcher on Linux
```

### Terminal Command

After installation:
```bash
openclaw --help
openclaw --version
openclaw create crew my-crew
# ... any iTaK CLI command
```

## Configuration

The adapter automatically detects:
- Python executable (python3, python, or py)
- Application resources location (dev vs packaged)
- iTaK source code location

## Uninstalling

### Removing Desktop App
Use standard OS uninstall procedures

### Removing Terminal Command

**macOS/Linux:**
```bash
sudo rm /usr/local/bin/openclaw
```

**Windows:**
Remove installation directory from PATH:
1. System Properties → Environment Variables
2. Edit System PATH
3. Remove OpenClaw installation directory

## Troubleshooting

### Python Not Found
Ensure Python 3.10+ is installed and in PATH:
```bash
python3 --version
```

### CLI Command Not Found (Terminal)
- Restart terminal after installation
- Check PATH includes installation directory
- Verify permissions on launcher script

### Application Won't Start
- Check Python installation
- Verify iTaK dependencies are installed
- Review console logs in DevTools (dev mode)

### Process Exit Protection
The adapter prevents CLI code from terminating Electron. Exit attempts are:
- Logged to console
- Emitted as events to renderer
- Displayed in UI logs

## Development Notes

### TypeScript Configuration
- `tsconfig.main.json` - Main and preload processes
- `tsconfig.renderer.json` - React renderer

### Build Process
1. TypeScript compilation (main/preload)
2. Vite bundling (renderer)
3. electron-builder packaging

### Asset Bundling
- Python source code bundled in `extraResources`
- Launcher scripts in `scripts/`
- Icons in `assets/` (update with real icons)

## Branding Assets

Logo source:
- Header: https://mintcdn.com/clawdhub/FaXdIfo7gPK_jSWb/assets/openclaw-logo-text.png

Icons to replace:
- `assets/icon.icns` (macOS)
- `assets/icon.ico` (Windows)  
- `assets/icon.png` (Linux)

## License

MIT - See parent project LICENSE file
