# iTaK Agent - Electron Desktop Application

This is the Electron-based desktop application for iTaK Agent Framework, providing a graphical dashboard for managing and monitoring your iTaK agents.

## Features

- 🖥️ **Cross-Platform Desktop App** - Works on macOS, Windows, and Linux
- 🎛️ **Intuitive Dashboard** - Visual interface for agent management
- 📊 **Real-Time Status** - Monitor agent status and performance
- 📝 **Live Logs** - View agent output in real-time
- 🎮 **Agent Controls** - Start, stop, and send commands to agents
- 🔧 **CLI Integration** - Bundled CLI accessible from system PATH

## Architecture

This Electron app integrates the iTaK CLI **in-process** by:

1. **Python CLI Wrapper**: Spawns the Python CLI as a child process
2. **IPC Bridge**: Main process communicates with renderer via Electron IPC
3. **React Dashboard**: Modern UI built with React and TypeScript
4. **System Integration**: Installer places CLI shim in system PATH

## Development

### Prerequisites

- Node.js 16+ 
- npm or pnpm
- Python 3.10+ (for iTaK CLI)
- The parent iTaK project must have `src/itak` directory

### Setup

```bash
# From the apps/electron directory
npm install

# Or from repository root
npm install --prefix apps/electron
```

### Running in Development Mode

```bash
# Start development server (runs renderer on port 5173 and Electron)
npm run dev

# Or from repository root
npm --prefix apps/electron run dev
```

The development server will:
- Launch Vite dev server for the renderer (http://localhost:5173)
- Compile and run the Electron main process
- Enable hot reload for renderer changes
- Open DevTools automatically

### Project Structure

```
apps/electron/
├── src/
│   ├── main.ts                 # Electron main process
│   ├── preload.ts              # Preload script (IPC bridge)
│   ├── cli-adapter/            # Python CLI wrapper
│   │   └── index.ts
│   ├── hooks/                  # React hooks
│   │   └── cli-adapter.ts      # Hook for CLI communication
│   └── renderer/               # React app
│       ├── index.html
│       ├── main.tsx            # React entry point
│       ├── Dashboard.tsx       # Main app component
│       ├── styles.css          # Global styles
│       └── pages/              # Page components
│           ├── WelcomePage.tsx
│           ├── StatusPage.tsx
│           ├── LogsPage.tsx
│           └── ControlsPage.tsx
├── installer-scripts/          # Platform-specific installer scripts
│   ├── mac/
│   ├── win/
│   └── linux/
├── scripts/
│   └── check-parent-build.js   # Pre-build validation
├── assets/                     # Application icons
├── package.json
├── tsconfig.main.json          # TypeScript config for main/preload
├── tsconfig.json               # TypeScript config for renderer
└── vite.config.ts              # Vite config for renderer
```

## Building

### Build for Development

```bash
# Build renderer and main process
npm run build
```

This will:
- Build the React renderer to `dist/renderer/`
- Compile TypeScript main process to `dist/main.js` and `dist/preload.js`

### Package for Distribution

```bash
# Package for current platform
npm run package

# Package for specific platforms
npm run package:mac     # macOS (DMG)
npm run package:win     # Windows (NSIS installer)
npm run package:linux   # Linux (AppImage, deb)
```

Built applications will be in the `release/` directory.

## CLI Integration

The installer places a CLI shim in the system PATH, allowing users to run `itak` commands from any terminal.

### How It Works

1. **Installer** copies the Python source to the app resources
2. **CLI Shim** is placed in system PATH:
   - **macOS**: `/usr/local/bin/itak` (script)
   - **Linux**: `/usr/local/bin/itak` (symlink to script)
   - **Windows**: Installer directory added to PATH (batch file)
3. **Shim Script** sets PYTHONPATH and executes the bundled CLI

### macOS Installation

The DMG installer:
- Installs app to `/Applications/iTaK Agent.app`
- Copies CLI shim to `/Applications/iTaK Agent.app/Contents/Resources/itak-cli.sh`
- **Manual step required**: User must run `sudo ln -s "/Applications/iTaK Agent.app/Contents/Resources/itak-cli.sh" /usr/local/bin/itak`

> **Note**: macOS DMG installers cannot automatically modify `/usr/local/bin` without admin privileges. Consider using a post-install script or PKG installer for automatic setup.

### Windows Installation

The NSIS installer:
- Installs app to `C:\Program Files\iTaK Agent` or user's choice
- Copies `itak.cmd` to install directory
- Adds install directory to system PATH (requires admin/UAC)

### Linux Installation

The DEB package:
- Installs app to `/opt/iTaK Agent`
- Post-install script (`postinst`) creates symlink: `/usr/local/bin/itak`
- Requires `python3` package dependency

The AppImage:
- Self-contained, no system installation
- CLI not automatically added to PATH (user must manually create link)

## Installer Configuration

Installer behavior is configured in `package.json` under the `build` section:

```json
{
  "build": {
    "appId": "com.itak.agent",
    "productName": "iTaK Agent",
    "mac": { ... },
    "win": { ... },
    "linux": { ... }
  }
}
```

### Customizing Icons

Replace placeholder icons in `assets/`:

- **icon.png**: 512x512 PNG (base icon)
- **icon.icns**: macOS icon (use `png2icns` or Icon Composer)
- **icon.ico**: Windows icon (256x256, with multiple sizes)

## Uninstallation

### macOS

```bash
# Remove application
rm -rf "/Applications/iTaK Agent.app"

# Remove CLI symlink
sudo rm /usr/local/bin/itak
```

### Windows

Use "Add or Remove Programs" in Windows Settings. The uninstaller will:
- Remove the application
- Remove the PATH entry

### Linux (DEB)

```bash
sudo apt remove itak-agent
sudo rm /usr/local/bin/itak  # If not removed automatically
```

### Linux (AppImage)

Simply delete the AppImage file.

## Permissions

### macOS

- The app requires **Accessibility** permissions if it needs to control other apps
- CLI installation to `/usr/local/bin` requires **admin privileges** (sudo)

### Windows

- The installer requires **UAC elevation** to modify system PATH
- Can be installed per-user without admin (PATH won't be system-wide)

### Linux

- DEB installation requires **sudo** for system-wide install and PATH setup
- AppImage can run without privileges but CLI won't be in PATH

## Troubleshooting

### "Python not found" error

Ensure Python 3.10+ is installed and in PATH:

```bash
python3 --version
# or
python --version
```

### CLI shim not working

**macOS/Linux**:
```bash
# Check if shim exists and is executable
ls -l /usr/local/bin/itak
which itak

# Make executable if needed
chmod +x /usr/local/bin/itak
```

**Windows**:
```cmd
# Check if install directory is in PATH
echo %PATH%

# Check if itak.cmd exists
dir "%ProgramFiles%\iTaK Agent\itak.cmd"
```

### Development mode: "Module not found" errors

Ensure parent project structure exists:

```bash
# From repository root
ls -la src/itak/
ls -la pyproject.toml
```

### Hot reload not working

- Renderer changes should hot reload automatically via Vite
- Main process changes require restarting the app (stop and run `npm run dev` again)

## CI/CD

A GitHub Actions workflow is provided in `.github/workflows/electron-build.yml` for automated builds.

The workflow:
- Installs dependencies
- Runs the build
- (Optional) Packages the app for all platforms
- (Optional) Uploads artifacts or creates releases

## Technology Stack

- **Electron 28**: Desktop app framework
- **TypeScript**: Type-safe development
- **React 18**: UI framework
- **Vite**: Fast build tool and dev server
- **React Router**: Client-side routing
- **electron-builder**: Packaging and installer creation
- **electron-log**: Logging library

## Contributing

When contributing to the Electron app:

1. Follow the existing code style (TypeScript, ESLint)
2. Test on all platforms if possible
3. Update documentation for new features
4. Ensure builds succeed before submitting PR

## License

MIT License - See repository root LICENSE file

## Support

For issues and questions:
- GitHub Issues: https://github.com/David2024patton/iTaK-Agent-Framework/issues
- Documentation: See repository root README.md
