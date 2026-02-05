/**
 * Electron Main Process for iTaK Agent Framework
 */

import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import log from 'electron-log';
import { cliAdapter, CliCommand } from './cli-adapter';

let mainWindow: BrowserWindow | null = null;

// Configure logging
log.transports.file.level = 'info';
log.transports.console.level = 'debug';

/**
 * Create the main application window
 */
function createMainWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
    titleBarStyle: 'default',
    backgroundColor: '#1a1a2e',
    show: false,
  });

  // Load the renderer
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * Setup IPC handlers for communication with renderer
 */
function setupIpcHandlers(): void {
  // Start agent handler
  ipcMain.handle('agent:start', async () => {
    log.info('IPC: Starting agent');
    try {
      const result = await cliAdapter.startAgent();
      return result;
    } catch (error) {
      log.error('Error starting agent:', error);
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  });

  // Stop agent handler
  ipcMain.handle('agent:stop', async () => {
    log.info('IPC: Stopping agent');
    try {
      const result = await cliAdapter.stopAgent();
      return result;
    } catch (error) {
      log.error('Error stopping agent:', error);
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  });

  // Run command handler
  ipcMain.handle('agent:command', async (_, command: CliCommand) => {
    log.info('IPC: Running command:', command);
    try {
      const result = await cliAdapter.runCommand(command);
      return result;
    } catch (error) {
      log.error('Error running command:', error);
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  });

  // Get status handler
  ipcMain.handle('agent:status', async () => {
    const status = cliAdapter.getStatus();
    return status;
  });

  // Get logs handler
  ipcMain.handle('agent:logs', async () => {
    const logs = cliAdapter.getLogs();
    return logs;
  });

  // Send input handler
  ipcMain.handle('agent:input', async (_, input: string) => {
    const success = cliAdapter.sendInput(input);
    return { success };
  });

  // Forward CLI adapter events to renderer
  cliAdapter.on('log', (data) => {
    mainWindow?.webContents.send('agent:log', data);
  });

  cliAdapter.on('agent-stopped', (data) => {
    mainWindow?.webContents.send('agent:stopped', data);
  });

  cliAdapter.on('agent-error', (error) => {
    mainWindow?.webContents.send('agent:error', {
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  });

  cliAdapter.on('command-output', (output) => {
    mainWindow?.webContents.send('command:output', output);
  });

  cliAdapter.on('command-error', (error) => {
    mainWindow?.webContents.send('command:error', error);
  });
}

/**
 * Application lifecycle handlers
 */
app.whenReady().then(() => {
  log.info('App is ready, creating window...');
  setupIpcHandlers();
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', async () => {
  log.info('App will quit, stopping agent...');
  try {
    await cliAdapter.stopAgent();
  } catch (error) {
    log.error('Error stopping agent on quit:', error);
  }
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  log.error('Uncaught exception:', error);
});

process.on('unhandledRejection', (reason) => {
  log.error('Unhandled rejection:', reason);
});
