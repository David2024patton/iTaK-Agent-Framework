# iTaK Electron Desktop Application

## Overview

The iTaK Electron app provides a cross-platform desktop application with a graphical dashboard for managing and monitoring iTaK agents. The app integrates the Python CLI in-process and includes installers that place the CLI in the system PATH for convenient command-line access.

## Quick Start

### For Developers

```bash
# Install dependencies
npm run electron:install

# Run in development mode
npm run electron:dev

# Build the app
npm run electron:build

# Package for distribution
npm run electron:package
```

### For End Users

Download the installer for your platform from the releases page:

- **macOS**: Download the `.dmg` file
- **Windows**: Download the `.exe` installer
- **Linux**: Download the `.AppImage` or `.deb` package

After installation, you can:
1. Launch the "iTaK Agent" desktop app from your applications
2. Use the `itak` command from any terminal (may require system restart on Windows)

## Architecture

### In-Process CLI Integration

The Electron app uses **Option B** (in-process integration) as specified in the requirements:

1. **Python CLI Spawning**: The Electron main process spawns the Python CLI as a child process
2. **No process.exit Calls**: The CLI runs in a controlled child process, preventing it from terminating the Electron app
3. **IPC Communication**: Main process communicates with renderer via secure IPC channels
4. **Event Streaming**: CLI output is streamed to the dashboard in real-time

### Components

- **Main Process** (`src/main.ts`): Electron main process, window management, IPC handlers
- **Preload Script** (`src/preload.ts`): Secure bridge between main and renderer processes
- **CLI Adapter** (`src/cli-adapter/index.ts`): Wraps Python CLI execution with safe error handling
- **React Dashboard** (`src/renderer/`): Modern UI built with React 18 and TypeScript
- **Installer Scripts** (`installer-scripts/`): Platform-specific scripts for CLI PATH integration

## CLI PATH Integration

The installers include scripts to add the `itak` CLI to the system PATH:

### macOS
- Installer: DMG with app bundle
- CLI Location: `/Applications/iTaK Agent.app/Contents/Resources/itak-cli.sh`
- PATH Setup: Manual symlink creation to `/usr/local/bin/itak` (requires sudo)

### Windows
- Installer: NSIS installer with UAC elevation
- CLI Location: `%ProgramFiles%\iTaK Agent\itak.cmd`
- PATH Setup: Installer adds directory to system PATH automatically

### Linux
- Installer: DEB package and AppImage
- CLI Location: `/opt/iTaK Agent/usr/bin/itak-cli.sh`
- PATH Setup: Post-install script creates symlink to `/usr/local/bin/itak`

## Development

See [apps/electron/README.md](apps/electron/README.md) for detailed development instructions.

### Technology Stack

- Electron 28 (Node.js 18)
- TypeScript 5.3
- React 18
- Vite 5 (build tool)
- React Router 6
- electron-builder (packaging)

### Color Scheme

The dashboard uses the iTaK color palette:
- Primary Background: `#0a0e27`
- Secondary Background: `#16213e`
- Accent Blue: `#0f4c75`
- Accent Cyan: `#3282b8`
- Accent Bright: `#00d4ff`

## CI/CD

The GitHub Actions workflow at `.github/workflows/electron-build.yml` automatically:
- Builds the app on push to main
- Tests on Ubuntu, macOS, and Windows
- (Optional) Creates release artifacts on workflow dispatch

## Compatibility

- **Electron**: 28.x (includes Node.js 18.x, Chromium 120.x)
- **Python**: 3.10+ (required for iTaK CLI)
- **Node.js**: 16+ (for building)
- **Platforms**: macOS 10.13+, Windows 10+, Ubuntu 18.04+

## Security Considerations

1. **Process Isolation**: CLI runs as separate child process, isolated from Electron
2. **Context Isolation**: Renderer process has no direct access to Node.js APIs
3. **IPC Security**: All main ↔ renderer communication goes through preload script
4. **Sandboxing**: Renderer runs in sandboxed mode

## Permissions

### macOS
- App signing required for distribution (Developer ID certificate)
- Notarization required for macOS 10.15+
- Manual CLI symlink creation requires sudo

### Windows
- Code signing recommended (Authenticode certificate)
- UAC elevation required for system-wide PATH modification
- Can install per-user without admin (PATH not system-wide)

### Linux
- DEB installation requires sudo
- AppImage runs without installation (CLI not in PATH unless manually configured)

## Known Limitations

1. **macOS CLI Setup**: Requires manual symlink creation due to DMG installer limitations
2. **Python Dependency**: Python 3.10+ must be installed separately
3. **First Launch**: May show security warnings on macOS/Windows if unsigned

## Future Enhancements

- [ ] Auto-update functionality
- [ ] Built-in Python runtime bundling
- [ ] Signed installers for all platforms
- [ ] Configuration UI for iTaK settings
- [ ] Multi-agent management
- [ ] Plugin system integration

## Support

For issues specific to the Electron app:
- Check [apps/electron/README.md](apps/electron/README.md) for troubleshooting
- Report bugs at: https://github.com/David2024patton/iTaK-Agent-Framework/issues

For general iTaK Framework support, see the main [README.md](README.md).
