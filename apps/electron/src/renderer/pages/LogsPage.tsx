import React from 'react';
import { useItakBridge } from '@hooks/cli-adapter';

export function LogsPage() {
  const { outputLines, wipeOutput } = useItakBridge();
  const logContainerRef = React.useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = React.useState(true);
  
  React.useEffect(() => {
    if (autoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [outputLines, autoScroll]);
  
  const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };
  
  return (
    <div>
      <div className="card">
        <div className="flex items-center justify-between mb-md">
          <h2 className="card-header" style={{ marginBottom: 0, paddingBottom: 0, border: 'none' }}>
            Agent Logs
          </h2>
          <div className="flex gap-sm">
            <label style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem',
              color: 'var(--itak-text-secondary)',
              cursor: 'pointer',
              fontSize: '0.9rem'
            }}>
              <input 
                type="checkbox" 
                checked={autoScroll}
                onChange={(e) => setAutoScroll(e.target.checked)}
              />
              Auto-scroll
            </label>
            <button 
              className="btn btn-primary"
              onClick={wipeOutput}
              style={{ fontSize: '0.85rem', padding: '0.25rem 0.75rem' }}
            >
              Clear Logs
            </button>
          </div>
        </div>
        
        <div className="log-viewer" ref={logContainerRef}>
          {outputLines.length === 0 ? (
            <div style={{ 
              textAlign: 'center', 
              color: 'var(--itak-text-muted)',
              padding: '2rem'
            }}>
              No logs yet. Start the agent to see output.
            </div>
          ) : (
            outputLines.map((line, idx) => (
              <div key={idx} className={`log-line ${line.stream}`}>
                <span className="log-timestamp">
                  [{formatTimestamp(line.time)}]
                </span>
                <span>{line.content}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
