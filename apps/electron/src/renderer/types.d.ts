// Type declarations for OpenClaw desktop app

interface CommandResult {
  success: boolean;
  output: string;
  error?: string;
  exitCode?: number;
}

interface AgentStatus {
  isRunning: boolean;
  outputBuffer: string[];
}

interface LogData {
  level: string;
  message: string;
}

interface ExitAttemptData {
  code?: number;
}

interface AgentStoppedData {
  exitCode: number | null;
}

interface OpenClawAPI {
  startAgent: () => Promise<CommandResult>;
  stopAgent: () => Promise<CommandResult>;
  runCommand: (args: string[]) => Promise<CommandResult>;
  getStatus: () => Promise<AgentStatus>;
  sendInput: (input: string) => Promise<boolean>;
  onLog: (callback: (data: LogData) => void) => () => void;
  onExitAttempt: (callback: (data: ExitAttemptData) => void) => () => void;
  onAgentStopped: (callback: (data: AgentStoppedData) => void) => () => void;
}

declare global {
  interface Window {
    openclaw: OpenClawAPI;
  }
}

export {};
