/**
 * Custom hook for iTaK CLI bridge communication
 */

import { useState, useEffect, useCallback, useReducer } from 'react';

export type ProcessState = {
  active: boolean;
  processId?: number;
  duration?: number;
};

export type OutputLine = {
  stream: 'stdout' | 'stderr' | 'info' | 'error';
  time: number;
  content: string;
};

type ActionType = 
  | { kind: 'ADD_OUTPUT'; payload: OutputLine }
  | { kind: 'CLEAR_ALL' }
  | { kind: 'TRIM_EXCESS'; maxLines: number };

function outputReducer(lines: OutputLine[], action: ActionType): OutputLine[] {
  switch (action.kind) {
    case 'ADD_OUTPUT':
      const newLines = [...lines, action.payload];
      return newLines.length > 500 ? newLines.slice(-500) : newLines;
    case 'CLEAR_ALL':
      return [];
    case 'TRIM_EXCESS':
      return lines.slice(-action.maxLines);
    default:
      return lines;
  }
}

export function useItakBridge() {
  const [processState, setProcessState] = useState<ProcessState>({ active: false });
  const [outputLines, dispatchOutput] = useReducer(outputReducer, []);
  const [busyFlag, setBusyFlag] = useState(false);

  const recordOutput = useCallback((stream: OutputLine['stream'], content: string) => {
    dispatchOutput({
      kind: 'ADD_OUTPUT',
      payload: { stream, time: Date.now(), content }
    });
  }, []);

  const pollProcessState = useCallback(async () => {
    try {
      const state = await window.itak.getStatus();
      setProcessState(state);
    } catch (err) {
      console.error('State polling failed:', err);
    }
  }, []);

  const initiateAgent = useCallback(async () => {
    setBusyFlag(true);
    try {
      const outcome = await window.itak.startAgent();
      if (outcome.success) {
        recordOutput('info', 'iTaK agent initialization complete');
        await pollProcessState();
      } else {
        recordOutput('error', outcome.error || 'Initialization failed');
      }
      return outcome;
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Unexpected error';
      recordOutput('error', `Initiation error: ${errMsg}`);
      return { success: false, output: '', error: errMsg };
    } finally {
      setBusyFlag(false);
    }
  }, [pollProcessState, recordOutput]);

  const terminateAgent = useCallback(async () => {
    setBusyFlag(true);
    try {
      const outcome = await window.itak.stopAgent();
      if (outcome.success) {
        recordOutput('info', 'Agent terminated');
        await pollProcessState();
      } else {
        recordOutput('error', outcome.error || 'Termination failed');
      }
      return outcome;
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Unexpected error';
      recordOutput('error', `Termination error: ${errMsg}`);
      return { success: false, output: '', error: errMsg };
    } finally {
      setBusyFlag(false);
    }
  }, [pollProcessState, recordOutput]);

  const executeCommand = useCallback(async (cmd: string, params?: string[]) => {
    setBusyFlag(true);
    const fullCmd = params ? `${cmd} ${params.join(' ')}` : cmd;
    recordOutput('info', `Executing: ${fullCmd}`);
    
    try {
      const outcome = await window.itak.runCommand(cmd, params);
      if (outcome.success) {
        recordOutput('stdout', outcome.output);
      } else {
        recordOutput('stderr', outcome.error || 'Execution failed');
      }
      return outcome;
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Unexpected error';
      recordOutput('error', `Execution error: ${errMsg}`);
      return { success: false, output: '', error: errMsg };
    } finally {
      setBusyFlag(false);
    }
  }, [recordOutput]);

  const transmitInput = useCallback(async (text: string) => {
    try {
      const outcome = await window.itak.sendInput(text);
      if (outcome.success) {
        recordOutput('info', `Input: ${text}`);
      }
      return outcome;
    } catch (err) {
      console.error('Input transmission failed:', err);
      return { success: false };
    }
  }, [recordOutput]);

  const wipeOutput = useCallback(() => {
    dispatchOutput({ kind: 'CLEAR_ALL' });
  }, []);

  useEffect(() => {
    const cleanupHandlers: Array<() => void> = [];

    cleanupHandlers.push(window.itak.onLog((evt) => {
      recordOutput(evt.type as OutputLine['stream'], evt.data);
    }));

    cleanupHandlers.push(window.itak.onAgentStopped((evt) => {
      recordOutput('info', `Process ended: code=${evt.code}, signal=${evt.signal}`);
      pollProcessState();
    }));

    cleanupHandlers.push(window.itak.onAgentError((evt) => {
      recordOutput('error', `Process error: ${evt.message}`);
      pollProcessState();
    }));

    cleanupHandlers.push(window.itak.onCommandOutput((text) => {
      recordOutput('stdout', text);
    }));

    cleanupHandlers.push(window.itak.onCommandError((text) => {
      recordOutput('stderr', text);
    }));

    pollProcessState();

    return () => {
      cleanupHandlers.forEach(cleanup => cleanup());
    };
  }, [pollProcessState, recordOutput]);

  return {
    processState,
    outputLines,
    busyFlag,
    initiateAgent,
    terminateAgent,
    executeCommand,
    transmitInput,
    pollProcessState,
    wipeOutput,
  };
}
