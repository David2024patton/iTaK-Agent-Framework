import React from 'react';
import { useItakBridge } from '@hooks/cli-adapter';

export function StatusPage() {
  const { processState, pollProcessState } = useItakBridge();
  
  React.useEffect(() => {
    const intervalId = setInterval(pollProcessState, 2000);
    return () => clearInterval(intervalId);
  }, [pollProcessState]);
  
  const formatUptime = (ms?: number) => {
    if (!ms) return 'N/A';
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  };
  
  return (
    <div>
      <div className="card">
        <h2 className="card-header">Agent Status</h2>
        
        <div className="flex flex-col gap-lg">
          <div className="flex items-center justify-between">
            <span style={{ color: 'var(--itak-text-secondary)' }}>Current State:</span>
            <span className={`status-badge ${processState.active ? 'running' : 'stopped'}`}>
              <span className={`status-indicator ${processState.active ? 'active' : 'inactive'}`}></span>
              {processState.active ? 'Running' : 'Stopped'}
            </span>
          </div>
          
          {processState.processId && (
            <div className="flex items-center justify-between">
              <span style={{ color: 'var(--itak-text-secondary)' }}>Process ID:</span>
              <code style={{ 
                backgroundColor: 'var(--itak-background-tertiary)',
                padding: '0.25rem 0.5rem',
                borderRadius: 'var(--radius-sm)',
                color: 'var(--itak-accent-bright)'
              }}>
                {processState.processId}
              </code>
            </div>
          )}
          
          <div className="flex items-center justify-between">
            <span style={{ color: 'var(--itak-text-secondary)' }}>Uptime:</span>
            <span style={{ color: 'var(--itak-text-primary)' }}>
              {formatUptime(processState.duration)}
            </span>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 className="card-header">System Information</h2>
        <div className="flex flex-col gap-md">
          <div className="flex items-center justify-between">
            <span style={{ color: 'var(--itak-text-secondary)' }}>Platform:</span>
            <span style={{ color: 'var(--itak-text-primary)' }}>
              {navigator.platform}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span style={{ color: 'var(--itak-text-secondary)' }}>User Agent:</span>
            <span style={{ 
              color: 'var(--itak-text-primary)',
              fontSize: '0.85rem',
              maxWidth: '400px',
              textAlign: 'right'
            }}>
              {navigator.userAgent.split(' ').slice(-2).join(' ')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
