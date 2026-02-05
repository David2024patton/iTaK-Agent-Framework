/**
 * Electron Adapter for iTaK CLI
 * 
 * This adapter provides a safe in-process wrapper around the Python-based iTaK CLI.
 * It spawns the Python CLI as a child process and provides programmatic APIs
 * for start/stop/runCommand operations while preventing process.exit calls
 * from terminating the Electron main process.
 */

import { spawn, ChildProcess } from 'child_process';
import { app } from 'electron';
import path from 'path';
import { EventEmitter } from 'events';

export interface ElectronAdapterOptions {
  pythonCommand?: string;
  workingDir?: string;
}

export interface CommandResult {
  success: boolean;
  output: string;
  error?: string;
  exitCode?: number;
}

export class ElectronAdapter extends EventEmitter {
  private pythonCommand: string;
  private workingDir: string;
  private cliProcess: ChildProcess | null = null;
  private isRunning: boolean = false;
  private outputBuffer: string[] = [];

  constructor(options: ElectronAdapterOptions = {}) {
    super();
    this.pythonCommand = options.pythonCommand || this.detectPythonCommand();
    
    // In production, the Python source is bundled in resources
    // In development, use the repository root
    if (app.isPackaged) {
      this.workingDir = path.join(process.resourcesPath, 'app');
    } else {
      this.workingDir = options.workingDir || path.join(__dirname, '../../../..');
    }
    
    this.setupProcessExitProtection();
  }

  /**
   * Detects available Python command (python3, python, py)
   */
  private detectPythonCommand(): string {
    const { execSync } = require('child_process');
    const commands = ['python3', 'python', 'py'];
    
    for (const cmd of commands) {
      try {
        execSync(`${cmd} --version`, { stdio: 'ignore' });
        return cmd;
      } catch (e) {
        continue;
      }
    }
    return 'python3'; // default fallback
  }

  /**
   * Patches process.exit to prevent child processes from killing Electron
   */
  private setupProcessExitProtection(): void {
    // Store original process.exit
    const originalExit = process.exit.bind(process);
    
    // Override process.exit to emit event instead of exiting
    process.exit = ((code?: number) => {
      this.emit('exit-attempt', { code });
      console.warn(`[ElectronAdapter] Prevented process.exit(${code}) call`);
      // Don't actually exit the Electron process
      // Instead, just log and continue
      return undefined as never;
    }) as typeof process.exit;
    
    // Store original for cleanup if needed
    (this as any)._originalExit = originalExit;
  }

  /**
   * Start the agent (interactive mode)
   */
  async startAgent(): Promise<CommandResult> {
    if (this.isRunning) {
      return {
        success: false,
        output: '',
        error: 'Agent is already running'
      };
    }

    return new Promise((resolve) => {
      try {
        // Start the CLI in interactive mode
        this.cliProcess = spawn(
          this.pythonCommand,
          ['-m', 'itak.cli.cli'],
          {
            cwd: this.workingDir,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true,
            env: { ...process.env }
          }
        );

        this.isRunning = true;
        this.outputBuffer = [];

        // Handle stdout
        this.cliProcess.stdout?.on('data', (data) => {
          const output = data.toString();
          this.outputBuffer.push(output);
          this.emit('log', { level: 'info', message: output });
        });

        // Handle stderr
        this.cliProcess.stderr?.on('data', (data) => {
          const output = data.toString();
          this.outputBuffer.push(output);
          this.emit('log', { level: 'error', message: output });
        });

        // Handle process exit
        this.cliProcess.on('exit', (code) => {
          this.isRunning = false;
          this.emit('agent-stopped', { exitCode: code });
        });

        // Give it a moment to start
        setTimeout(() => {
          resolve({
            success: true,
            output: 'Agent started successfully'
          });
        }, 1000);

      } catch (error) {
        this.isRunning = false;
        resolve({
          success: false,
          output: '',
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    });
  }

  /**
   * Stop the running agent
   */
  async stopAgent(): Promise<CommandResult> {
    if (!this.isRunning || !this.cliProcess) {
      return {
        success: false,
        output: '',
        error: 'Agent is not running'
      };
    }

    return new Promise((resolve) => {
      if (this.cliProcess) {
        this.cliProcess.once('exit', () => {
          this.isRunning = false;
          this.cliProcess = null;
          resolve({
            success: true,
            output: 'Agent stopped successfully'
          });
        });

        // Send SIGTERM
        this.cliProcess.kill('SIGTERM');

        // Force kill after 5 seconds if still running
        setTimeout(() => {
          if (this.cliProcess && this.isRunning) {
            this.cliProcess.kill('SIGKILL');
          }
        }, 5000);
      }
    });
  }

  /**
   * Run a CLI command
   */
  async runCommand(args: string[]): Promise<CommandResult> {
    return new Promise((resolve) => {
      try {
        const process = spawn(
          this.pythonCommand,
          ['-m', 'itak.cli.cli', ...args],
          {
            cwd: this.workingDir,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true,
            env: { ...process.env }
          }
        );

        let stdout = '';
        let stderr = '';

        process.stdout?.on('data', (data) => {
          const output = data.toString();
          stdout += output;
          this.emit('log', { level: 'info', message: output });
        });

        process.stderr?.on('data', (data) => {
          const output = data.toString();
          stderr += output;
          this.emit('log', { level: 'error', message: output });
        });

        process.on('exit', (code) => {
          resolve({
            success: code === 0,
            output: stdout,
            error: stderr || undefined,
            exitCode: code || undefined
          });
        });

        process.on('error', (error) => {
          resolve({
            success: false,
            output: stdout,
            error: error.message,
            exitCode: 1
          });
        });

      } catch (error) {
        resolve({
          success: false,
          output: '',
          error: error instanceof Error ? error.message : 'Unknown error',
          exitCode: 1
        });
      }
    });
  }

  /**
   * Get current status
   */
  getStatus(): { isRunning: boolean; outputBuffer: string[] } {
    return {
      isRunning: this.isRunning,
      outputBuffer: [...this.outputBuffer]
    };
  }

  /**
   * Send input to running agent
   */
  sendInput(input: string): boolean {
    if (!this.cliProcess || !this.isRunning) {
      return false;
    }
    
    try {
      this.cliProcess.stdin?.write(input + '\n');
      return true;
    } catch (error) {
      console.error('Failed to send input:', error);
      return false;
    }
  }

  /**
   * Cleanup
   */
  async cleanup(): Promise<void> {
    if (this.isRunning) {
      await this.stopAgent();
    }
  }
}
