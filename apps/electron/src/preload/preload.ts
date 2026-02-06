/**
 * OpenClaw Desktop - Preload Script
 * 
 * Exposes safe IPC APIs to the renderer process via contextBridge
 */

import { contextBridge, ipcRenderer } from 'electron';

export interface OpenClawAPI {
  startAgent: () => Promise<{ success: boolean; output: string; error?: string }>;
  stopAgent: () => Promise<{ success: boolean; output: string; error?: string }>;
  runCommand: (args: string[]) => Promise<{
    success: boolean;
    output: string;
    error?: string;
    exitCode?: number;
  }>;
  getStatus: () => Promise<{ isRunning: boolean; outputBuffer: string[] }>;
  sendInput: (input: string) => Promise<boolean>;
  onLog: (callback: (data: { level: string; message: string }) => void) => () => void;
  onExitAttempt: (callback: (data: { code?: number }) => void) => () => void;
  onAgentStopped: (callback: (data: { exitCode: number | null }) => void) => () => void;
}

const api: OpenClawAPI = {
  startAgent: () => ipcRenderer.invoke('start-agent'),
  stopAgent: () => ipcRenderer.invoke('stop-agent'),
  runCommand: (args: string[]) => ipcRenderer.invoke('run-command', args),
  getStatus: () => ipcRenderer.invoke('get-status'),
  sendInput: (input: string) => ipcRenderer.invoke('send-input', input),
  
  onLog: (callback) => {
    const listener = (_event: any, data: any) => callback(data);
    ipcRenderer.on('agent-log', listener);
    return () => ipcRenderer.removeListener('agent-log', listener);
  },
  
  onExitAttempt: (callback) => {
    const listener = (_event: any, data: any) => callback(data);
    ipcRenderer.on('exit-attempt', listener);
    return () => ipcRenderer.removeListener('exit-attempt', listener);
  },
  
  onAgentStopped: (callback) => {
    const listener = (_event: any, data: any) => callback(data);
    ipcRenderer.on('agent-stopped', listener);
    return () => ipcRenderer.removeListener('agent-stopped', listener);
  }
};

contextBridge.exposeInMainWorld('openclaw', api);

// Type declaration for window.openclaw
declare global {
  interface Window {
    openclaw: OpenClawAPI;
  }
}
