# iTaK Electron App - Quick Start Guide

## For Developers

### Installation

```bash
# From repository root
npm run electron:install
```

### Development

```bash
# Start development server (hot reload enabled)
npm run electron:dev
```

This will:
1. Start Vite dev server on http://localhost:5173
2. Launch Electron with DevTools
3. Watch for changes and auto-reload

### Building

```bash
# Build for production
npm run electron:build

# Package installers
npm run electron:package           # Current platform
npm run electron:package:mac       # macOS DMG
npm run electron:package:win       # Windows installer
npm run electron:package:linux     # Linux DEB + AppImage
```

Built packages will be in `apps/electron/release/`

### Project Structure

```
apps/electron/
├── src/
│   ├── main.ts              # Electron main process
│   ├── preload.ts           # IPC bridge
│   ├── cli-adapter/         # Python CLI wrapper
│   │   └── index.ts
│   ├── hooks/               # React hooks
│   │   └── cli-adapter.ts
│   └── renderer/            # React UI
│       ├── Dashboard.tsx
│       ├── main.tsx
│       ├── styles.css
│       └── pages/
│           ├── WelcomePage.tsx
│           ├── StatusPage.tsx
│           ├── LogsPage.tsx
│           └── ControlsPage.tsx
└── installer-scripts/       # Platform installers
```

## For End Users

### Installation

#### macOS
1. Download `iTaK-Agent-X.X.X.dmg`
2. Open DMG and drag app to Applications
3. Open Terminal and run:
   ```bash
   sudo ln -s "/Applications/iTaK Agent.app/Contents/Resources/itak-cli.sh" /usr/local/bin/itak
   ```
4. Verify: `itak --version`

#### Windows
1. Download `iTaK-Agent-Setup-X.X.X.exe`
2. Run installer (requires admin - UAC prompt)
3. Choose install location
4. Installer will add CLI to PATH
5. Restart terminal or computer
6. Verify: `itak --version`

#### Linux (DEB)
1. Download `itak-agent_X.X.X_amd64.deb`
2. Install:
   ```bash
   sudo dpkg -i itak-agent_X.X.X_amd64.deb
   ```
3. Verify: `itak --version`

#### Linux (AppImage)
1. Download `iTaK-Agent-X.X.X.AppImage`
2. Make executable:
   ```bash
   chmod +x iTaK-Agent-X.X.X.AppImage
   ```
3. Run: `./iTaK-Agent-X.X.X.AppImage`

> Note: AppImage doesn't install CLI to PATH automatically

### Using the App

1. **Launch**: Find "iTaK Agent" in your applications
2. **Welcome**: See overview and quick actions
3. **Status**: Monitor agent state and uptime
4. **Logs**: View real-time output
5. **Controls**: Start/stop agent, run commands

### Using the CLI

After installation, the `itak` command is available system-wide:

```bash
# Show version
itak --version

# Create a crew
itak create my-crew

# Run a crew
itak run my-crew

# Interactive mode
itak
```

## Requirements

### System Requirements
- **macOS**: 10.13 or later
- **Windows**: 10 or later
- **Linux**: Ubuntu 18.04+ or equivalent

### Dependencies
- **Python**: 3.10 or higher (must be installed separately)
- **Node.js**: Bundled with Electron (no separate install needed)

### Disk Space
- Application: ~200 MB
- Plus dependencies if installed via npm

## Troubleshooting

### "Python not found"

Install Python 3.10+:

**macOS**:
```bash
brew install python@3.11
```

**Windows**:
Download from https://www.python.org/downloads/

**Linux**:
```bash
sudo apt install python3.11
```

### CLI not in PATH (macOS)

Create symlink manually:
```bash
sudo ln -s "/Applications/iTaK Agent.app/Contents/Resources/itak-cli.sh" /usr/local/bin/itak
```

### CLI not in PATH (Windows)

1. Open "Edit system environment variables"
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Add: `C:\Program Files\iTaK Agent`
5. Restart terminal

### App won't open (macOS)

First launch may show security warning:
1. Right-click app → "Open"
2. Click "Open" in dialog
3. Or: System Preferences → Security & Privacy → "Open Anyway"

### App won't open (Windows)

Windows Defender SmartScreen may show warning:
1. Click "More info"
2. Click "Run anyway"

> Note: Code signing will eliminate these warnings in production

## Development Tips

### Hot Reload

- **Renderer**: Changes auto-reload via Vite
- **Main Process**: Restart app manually (Ctrl+C, then `npm run dev`)

### Debugging

- **Renderer**: DevTools open automatically in dev mode
- **Main Process**: Use `console.log()` (outputs to terminal)
- **CLI**: Check logs in UI or terminal output

### Testing CLI Integration

```bash
# From apps/electron
npm run dev

# In app UI:
# 1. Go to Controls page
# 2. Click "Start Agent"
# 3. Check Logs page for output
```

## Support

- **Documentation**: See `apps/electron/README.md`
- **Issues**: https://github.com/David2024patton/iTaK-Agent-Framework/issues
- **Architecture**: See `docs/ELECTRON_APP.md`

## Version History

- **0.1.0** (Current): Initial release with basic dashboard and CLI integration

---

**Need Help?** Check the comprehensive README at `apps/electron/README.md`
