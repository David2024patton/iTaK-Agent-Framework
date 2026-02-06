/**
 * OpenClaw Desktop - Electron Main Process
 * 
 * Main process for the Electron wrapper around iTaK CLI
 */

import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import { ElectronAdapter } from '../electron-adapter.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow: BrowserWindow | null = null;
let adapter: ElectronAdapter | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, '../preload/preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    title: 'OpenClaw Desktop',
    autoHideMenuBar: true
  });

  // Load the renderer
  if (app.isPackaged) {
    // Production: load the built files
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  } else {
    // Development: load from Vite dev server or built files
    const rendererPath = path.join(__dirname, '../renderer/index.html');
    mainWindow.loadFile(rendererPath);
  }

  // Open DevTools in development
  if (!app.isPackaged) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function setupAdapter() {
  adapter = new ElectronAdapter();

  // Forward logs to renderer
  adapter.on('log', (data) => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('agent-log', data);
    }
  });

  // Forward exit attempts
  adapter.on('exit-attempt', (data) => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('exit-attempt', data);
    }
  });

  // Forward agent stopped event
  adapter.on('agent-stopped', (data) => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('agent-stopped', data);
    }
  });
}

function setupIPC() {
  // Start agent
  ipcMain.handle('start-agent', async () => {
    if (!adapter) {
      return { success: false, error: 'Adapter not initialized' };
    }
    return await adapter.startAgent();
  });

  // Stop agent
  ipcMain.handle('stop-agent', async () => {
    if (!adapter) {
      return { success: false, error: 'Adapter not initialized' };
    }
    return await adapter.stopAgent();
  });

  // Run command
  ipcMain.handle('run-command', async (_event, args: string[]) => {
    if (!adapter) {
      return { success: false, error: 'Adapter not initialized' };
    }
    return await adapter.runCommand(args);
  });

  // Get status
  ipcMain.handle('get-status', async () => {
    if (!adapter) {
      return { isRunning: false, outputBuffer: [] };
    }
    return adapter.getStatus();
  });

  // Send input to running agent
  ipcMain.handle('send-input', async (_event, input: string) => {
    if (!adapter) {
      return false;
    }
    return adapter.sendInput(input);
  });
}

// App lifecycle
app.whenReady().then(() => {
  setupAdapter();
  setupIPC();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', async () => {
  if (adapter) {
    await adapter.cleanup();
  }
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  // Don't exit - this is the protection we want
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection at:', promise, 'reason:', reason);
  // Don't exit - this is the protection we want
});
