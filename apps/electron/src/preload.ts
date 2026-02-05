/**
 * Preload script for iTaK Electron App
 * Exposes safe IPC API to the renderer process
 */

import { contextBridge, ipcRenderer } from 'electron';

export interface ItakApi {
  // Agent control
  startAgent: () => Promise<{ success: boolean; output: string; error?: string }>;
  stopAgent: () => Promise<{ success: boolean; output: string; error?: string }>;
  
  // Command execution
  runCommand: (command: string, args?: string[]) => Promise<{
    success: boolean;
    output: string;
    error?: string;
  }>;
  
  // Status and logs
  getStatus: () => Promise<{
    running: boolean;
    pid?: number;
    uptime?: number;
  }>;
  
  getLogs: () => Promise<{
    output: string[];
    errors: string[];
  }>;
  
  sendInput: (input: string) => Promise<{ success: boolean }>;
  
  // Event subscriptions
  onLog: (callback: (data: { type: string; data: string }) => void) => () => void;
  onAgentStopped: (callback: (data: { code: number | null; signal: string | null }) => void) => () => void;
  onAgentError: (callback: (data: { message: string }) => void) => () => void;
  onCommandOutput: (callback: (output: string) => void) => () => void;
  onCommandError: (callback: (error: string) => void) => () => void;
}

// Expose protected API to renderer
const itakApi: ItakApi = {
  startAgent: () => ipcRenderer.invoke('agent:start'),
  
  stopAgent: () => ipcRenderer.invoke('agent:stop'),
  
  runCommand: (command: string, args?: string[]) => 
    ipcRenderer.invoke('agent:command', { command, args }),
  
  getStatus: () => ipcRenderer.invoke('agent:status'),
  
  getLogs: () => ipcRenderer.invoke('agent:logs'),
  
  sendInput: (input: string) => ipcRenderer.invoke('agent:input', input),
  
  onLog: (callback) => {
    const listener = (_: any, data: any) => callback(data);
    ipcRenderer.on('agent:log', listener);
    return () => ipcRenderer.removeListener('agent:log', listener);
  },
  
  onAgentStopped: (callback) => {
    const listener = (_: any, data: any) => callback(data);
    ipcRenderer.on('agent:stopped', listener);
    return () => ipcRenderer.removeListener('agent:stopped', listener);
  },
  
  onAgentError: (callback) => {
    const listener = (_: any, data: any) => callback(data);
    ipcRenderer.on('agent:error', listener);
    return () => ipcRenderer.removeListener('agent:error', listener);
  },
  
  onCommandOutput: (callback) => {
    const listener = (_: any, output: string) => callback(output);
    ipcRenderer.on('command:output', listener);
    return () => ipcRenderer.removeListener('command:output', listener);
  },
  
  onCommandError: (callback) => {
    const listener = (_: any, error: string) => callback(error);
    ipcRenderer.on('command:error', listener);
    return () => ipcRenderer.removeListener('command:error', listener);
  },
};

contextBridge.exposeInMainWorld('itak', itakApi);

// Type declaration for TypeScript
declare global {
  interface Window {
    itak: ItakApi;
  }
}
