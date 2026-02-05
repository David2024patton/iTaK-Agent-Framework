import React, { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

interface LogEntry {
  id: number;
  level: string;
  message: string;
  timestamp: Date;
}

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [commandInput, setCommandInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(true);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const logIdCounter = useRef(0);

  useEffect(() => {
    // Check initial status
    window.openclaw.getStatus().then(status => {
      setIsRunning(status.isRunning);
      if (status.isRunning) {
        setShowOnboarding(false);
      }
    });

    // Set up log listener
    const unsubscribeLog = window.openclaw.onLog((data) => {
      const newLog: LogEntry = {
        id: logIdCounter.current++,
        level: data.level,
        message: data.message,
        timestamp: new Date()
      };
      setLogs(prev => [...prev, newLog]);
    });

    // Set up agent stopped listener
    const unsubscribeAgentStopped = window.openclaw.onAgentStopped(() => {
      setIsRunning(false);
      addSystemLog('Agent stopped');
    });

    // Set up exit attempt listener
    const unsubscribeExitAttempt = window.openclaw.onExitAttempt((data) => {
      addSystemLog(`Exit attempt intercepted (code: ${data.code})`);
    });

    return () => {
      unsubscribeLog();
      unsubscribeAgentStopped();
      unsubscribeExitAttempt();
    };
  }, []);

  useEffect(() => {
    // Auto-scroll logs
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const addSystemLog = (message: string) => {
    const newLog: LogEntry = {
      id: logIdCounter.current++,
      level: 'system',
      message,
      timestamp: new Date()
    };
    setLogs(prev => [...prev, newLog]);
  };

  const handleStartAgent = async () => {
    setIsLoading(true);
    try {
      const result = await window.openclaw.startAgent();
      if (result.success) {
        setIsRunning(true);
        setShowOnboarding(false);
        addSystemLog('Agent started successfully');
      } else {
        addSystemLog(`Failed to start agent: ${result.error}`);
      }
    } catch (error) {
      addSystemLog(`Error starting agent: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopAgent = async () => {
    setIsLoading(true);
    try {
      const result = await window.openclaw.stopAgent();
      if (result.success) {
        setIsRunning(false);
        addSystemLog('Agent stopped successfully');
      } else {
        addSystemLog(`Failed to stop agent: ${result.error}`);
      }
    } catch (error) {
      addSystemLog(`Error stopping agent: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRunCommand = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commandInput.trim()) return;

    setIsLoading(true);
    addSystemLog(`Running command: ${commandInput}`);
    
    try {
      const args = commandInput.trim().split(' ');
      const result = await window.openclaw.runCommand(args);
      
      if (result.success) {
        addSystemLog('Command completed successfully');
      } else {
        addSystemLog(`Command failed: ${result.error}`);
      }
    } catch (error) {
      addSystemLog(`Error running command: ${error}`);
    } finally {
      setIsLoading(false);
      setCommandInput('');
    }
  };

  const handleClearLogs = () => {
    setLogs([]);
  };

  return (
    <div className="app">
      <header className="header">
        <img 
          src="https://mintcdn.com/clawdhub/FaXdIfo7gPK_jSWb/assets/openclaw-logo-text.png?w=1650&fit=max&auto=format&n=FaXdIfo7gPK_jSWb&q=85&s=e82a8bd9b834bec4f6e97303deb1735b" 
          alt="OpenClaw Logo" 
          className="logo"
        />
        <div className="status-indicator">
          <span className={`status-dot ${isRunning ? 'running' : 'stopped'}`}></span>
          <span className="status-text">{isRunning ? 'Running' : 'Stopped'}</span>
        </div>
      </header>

      <main className="main-content">
        {showOnboarding && (
          <div className="onboarding">
            <h2>Welcome to OpenClaw Desktop</h2>
            <p>
              OpenClaw is a desktop wrapper for the iTaK Agent Framework CLI.
              Get started by launching the agent or running CLI commands.
            </p>
            <div className="onboarding-actions">
              <button 
                className="btn btn-primary btn-large"
                onClick={handleStartAgent}
                disabled={isLoading}
              >
                {isLoading ? 'Starting...' : 'Start Agent'}
              </button>
            </div>
          </div>
        )}

        {!showOnboarding && (
          <>
            <div className="controls">
              <div className="control-group">
                <button
                  className={`btn ${isRunning ? 'btn-danger' : 'btn-primary'}`}
                  onClick={isRunning ? handleStopAgent : handleStartAgent}
                  disabled={isLoading}
                >
                  {isLoading ? '...' : isRunning ? 'Stop Agent' : 'Start Agent'}
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={handleClearLogs}
                  disabled={isLoading}
                >
                  Clear Logs
                </button>
              </div>

              <form onSubmit={handleRunCommand} className="command-form">
                <input
                  type="text"
                  className="command-input"
                  placeholder="Enter CLI command (e.g., --version, --help)"
                  value={commandInput}
                  onChange={(e) => setCommandInput(e.target.value)}
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={isLoading || !commandInput.trim()}
                >
                  Run
                </button>
              </form>
            </div>

            <div className="logs-container">
              <div className="logs-header">
                <h3>Logs</h3>
                <span className="logs-count">{logs.length} entries</span>
              </div>
              <div className="logs">
                {logs.length === 0 ? (
                  <div className="logs-empty">No logs yet. Start the agent or run a command.</div>
                ) : (
                  logs.map((log) => (
                    <div key={log.id} className={`log-entry log-${log.level}`}>
                      <span className="log-timestamp">
                        {log.timestamp.toLocaleTimeString()}
                      </span>
                      <span className="log-level">[{log.level.toUpperCase()}]</span>
                      <span className="log-message">{log.message}</span>
                    </div>
                  ))
                )}
                <div ref={logsEndRef} />
              </div>
            </div>
          </>
        )}
      </main>

      <footer className="footer">
        <p>OpenClaw Desktop v0.1.0 | iTaK Agent Framework</p>
      </footer>
    </div>
  );
}

// Initialize React app
const root = createRoot(document.getElementById('root')!);
root.render(<App />);
