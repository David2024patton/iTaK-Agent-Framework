/**
 * CLI Adapter for iTaK Electron App
 * 
 * This adapter wraps the Python CLI and prevents process.exit calls
 * by running the CLI in a child process and communicating via IPC.
 */

import { spawn, ChildProcess } from 'child_process';
import { EventEmitter } from 'events';
import * as path from 'path';
import * as fs from 'fs';
import log from 'electron-log';

export interface CliCommand {
  command: string;
  args?: string[];
}

export interface CliResponse {
  success: boolean;
  output: string;
  error?: string;
}

export interface AgentStatus {
  running: boolean;
  pid?: number;
  uptime?: number;
}

class CliAdapter extends EventEmitter {
  private process: ChildProcess | null = null;
  private pythonPath: string = 'python3';
  private itakModulePath: string;
  private startTime: number | null = null;
  private outputBuffer: string[] = [];
  private errorBuffer: string[] = [];

  constructor() {
    super();
    
    // Determine iTaK module path based on app.isPackaged
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      // In development, reference the parent repository
      this.itakModulePath = path.join(__dirname, '..', '..', '..', '..');
    } else {
      // In production, use bundled resources
      this.itakModulePath = path.join(process.resourcesPath, 'python-src');
    }
    
    this.detectPythonCommand();
  }

  /**
   * Detect available Python command
   */
  private detectPythonCommand(): void {
    const candidates = ['python3', 'python', 'py'];
    const { execSync } = require('child_process');
    
    for (const cmd of candidates) {
      try {
        execSync(`${cmd} --version`, { stdio: 'ignore' });
        this.pythonPath = cmd;
        log.info(`Using Python command: ${cmd}`);
        return;
      } catch {
        continue;
      }
    }
    
    log.warn('No Python command found, defaulting to python3');
    this.pythonPath = 'python3';
  }

  /**
   * Start the iTaK agent in REPL mode
   */
  async startAgent(): Promise<CliResponse> {
    if (this.process) {
      return {
        success: false,
        output: '',
        error: 'Agent already running',
      };
    }

    return new Promise((resolve) => {
      try {
        // Launch Python CLI in interactive mode
        this.process = spawn(this.pythonPath, ['-m', 'itak.cli.cli'], {
          cwd: this.itakModulePath,
          stdio: ['pipe', 'pipe', 'pipe'],
          shell: true,
          env: {
            ...process.env,
            PYTHONUNBUFFERED: '1',
            ITAK_ELECTRON_MODE: '1',
          },
        });

        this.startTime = Date.now();
        this.setupProcessHandlers();

        resolve({
          success: true,
          output: 'Agent started successfully',
        });
      } catch (error) {
        log.error('Failed to start agent:', error);
        resolve({
          success: false,
          output: '',
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    });
  }

  /**
   * Stop the running agent
   */
  async stopAgent(): Promise<CliResponse> {
    if (!this.process) {
      return {
        success: false,
        output: '',
        error: 'No agent running',
      };
    }

    return new Promise((resolve) => {
      if (!this.process) {
        resolve({ success: false, output: '', error: 'Process not found' });
        return;
      }

      const timeout = setTimeout(() => {
        if (this.process) {
          this.process.kill('SIGKILL');
        }
      }, 5000);

      this.process.once('exit', () => {
        clearTimeout(timeout);
        this.cleanup();
        resolve({
          success: true,
          output: 'Agent stopped',
        });
      });

      this.process.kill('SIGTERM');
    });
  }

  /**
   * Execute a CLI command
   */
  async runCommand(cmd: CliCommand): Promise<CliResponse> {
    return new Promise((resolve) => {
      const allArgs = ['-m', 'itak.cli.cli', cmd.command, ...(cmd.args || [])];
      
      const cmdProcess = spawn(this.pythonPath, allArgs, {
        cwd: this.itakModulePath,
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true,
        env: {
          ...process.env,
          PYTHONUNBUFFERED: '1',
        },
      });

      let outputData = '';
      let errorData = '';

      cmdProcess.stdout?.on('data', (data) => {
        const text = data.toString();
        outputData += text;
        this.emit('command-output', text);
      });

      cmdProcess.stderr?.on('data', (data) => {
        const text = data.toString();
        errorData += text;
        this.emit('command-error', text);
      });

      cmdProcess.on('close', (code) => {
        resolve({
          success: code === 0,
          output: outputData,
          error: code !== 0 ? errorData : undefined,
        });
      });

      cmdProcess.on('error', (err) => {
        resolve({
          success: false,
          output: '',
          error: err.message,
        });
      });
    });
  }

  /**
   * Get current agent status
   */
  getStatus(): AgentStatus {
    return {
      running: this.process !== null && !this.process.killed,
      pid: this.process?.pid,
      uptime: this.startTime ? Date.now() - this.startTime : undefined,
    };
  }

  /**
   * Get recent logs
   */
  getLogs(): { output: string[]; errors: string[] } {
    return {
      output: [...this.outputBuffer],
      errors: [...this.errorBuffer],
    };
  }

  /**
   * Send input to the running agent
   */
  sendInput(input: string): boolean {
    if (!this.process || !this.process.stdin) {
      return false;
    }

    try {
      this.process.stdin.write(input + '\n');
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Setup process event handlers
   */
  private setupProcessHandlers(): void {
    if (!this.process) return;

    this.process.stdout?.on('data', (data) => {
      const text = data.toString();
      this.outputBuffer.push(text);
      if (this.outputBuffer.length > 1000) {
        this.outputBuffer.shift();
      }
      this.emit('log', { type: 'stdout', data: text });
    });

    this.process.stderr?.on('data', (data) => {
      const text = data.toString();
      this.errorBuffer.push(text);
      if (this.errorBuffer.length > 1000) {
        this.errorBuffer.shift();
      }
      this.emit('log', { type: 'stderr', data: text });
    });

    this.process.on('exit', (code, signal) => {
      log.info(`Agent process exited with code ${code}, signal ${signal}`);
      this.emit('agent-stopped', { code, signal });
      this.cleanup();
    });

    this.process.on('error', (err) => {
      log.error('Agent process error:', err);
      this.emit('agent-error', err);
      this.cleanup();
    });
  }

  /**
   * Cleanup resources
   */
  private cleanup(): void {
    this.process = null;
    this.startTime = null;
  }
}

// Export singleton instance
export const cliAdapter = new CliAdapter();
